obs         = obslua
script_enabled = false
source_name = ""
source_scene_name = ""
source_scene_time = 20
hotkey_id   = obs.OBS_INVALID_HOTKEY_ID
attempts    = 0
replaying   = false

----------------------------------------------------------

-- Toggle scene
function show_replay(visible)
	if visible == true then
		replaying = true
	else
		replaying = false
	end
	local scenes = obs.obs_frontend_get_scenes()
	if scenes ~= nil then
		for _, scene in ipairs(scenes) do
			if obs.obs_source_get_name(scene) == source_scene_name then
				scene = obs.obs_scene_from_source(scene)
				local items = obs.obs_scene_enum_items(scene)
				for _,item in ipairs(items) do
					if item ~= nil then
						scene_source = obs.obs_sceneitem_get_source(item)
						local sceneItem = obs.obs_scene_find_sceneitem_by_id(scene, obs.obs_sceneitem_get_id(item))
						obs.obs_sceneitem_set_visible(sceneItem, visible)
					end
				end
			end
		end
	end
	obs.source_list_release(scenes)
end

-- Stop replay timer
function stop_replay()
  attempts = attempts + 1
  if source_scene_time == nul or source_scene_time < 1 then
  	source_scene_time = 1
  end
  if attempts >= source_scene_time then
  	show_replay(false)
  	obs.remove_current_callback()
  end
  
--	local source = obs.obs_get_source_by_name(source_name)
--	if source ~= nil then
--		settings = obs.obs_source_get_settings(source)
--		obs.script_log(obs.LOG_WARNING,obs.obs_data_get_string(settings, "local_file"))
--		obs.obs_data_save_json(settings, 'd:\\json')
--		obs.obs_data_release(settings)
--		obs.obs_source_release(source)
--	end
end

-- Play replay
function try_play()
	local replay_buffer = obs.obs_frontend_get_replay_buffer_output()
	if replay_buffer == nil then
		show_replay(false)
		obs.remove_current_callback()
		return
	end
	show_replay(true)
	-- Call the procedure of the replay buffer named "get_last_replay" to
	-- get the last replay created by the replay buffer
	local cd = obs.calldata_create()
	local ph = obs.obs_output_get_proc_handler(replay_buffer)
	obs.proc_handler_call(ph, "get_last_replay", cd)
	local path = obs.calldata_string(cd, "path")
	obs.calldata_destroy(cd)

	obs.obs_output_release(replay_buffer)

	-- If the path is valid and the source exists, update it with the
	-- replay file to play back the replay.  Otherwise, stop attempting to
	-- replay after 10 seconds
	if path == nil then
		attempts = attempts + 1
		if attempts >= 10 then
			show_replay(false)
			obs.remove_current_callback()
		end
	else
		local source = obs.obs_get_source_by_name(source_name)
		if source ~= nil then
			local settings = obs.obs_data_create()
			obs.obs_data_set_string(settings, "local_file", path)
			obs.obs_data_get_bool(settings, "active")
			obs.obs_data_set_bool(settings, "close_when_inactive", true)
			obs.obs_data_set_bool(settings, "restart_on_activate", true)

			-- updating will automatically cause the source to
			-- refresh if the source is currently active, otherwise
			-- the source will play whenever its scene is activated
			obs.obs_source_update(source, settings)

			obs.obs_data_release(settings)
			obs.obs_source_release(source)
			
			attempts = 0
			obs.timer_add(stop_replay, 1000)
		end

		obs.remove_current_callback()
	end
end

-- The "Instant Replay" hotkey callback
function obs_instant_replay(pressed)
	if not pressed then
		return
	end
	
	if script_enabled == false then
		return
	end
	
	if replaying == true then
		return
	end

	local replay_buffer = obs.obs_frontend_get_replay_buffer_output()
	if replay_buffer ~= nil then
		-- Call the procedure of the replay buffer named "get_last_replay" to
		-- get the last replay created by the replay buffer
		local ph = obs.obs_output_get_proc_handler(replay_buffer)
		obs.proc_handler_call(ph, "save", nil)

		-- Set a 1-second timer to attempt playback every 1 second
		-- until the replay is available
		if obs.obs_output_active(replay_buffer) then
			attempts = 0
			obs.timer_add(try_play, 1000)
		else
			obs.script_log(obs.LOG_WARNING, "Tried to save an instant replay, but the replay buffer is not active!")
		end

		obs.obs_output_release(replay_buffer)
	else
		obs.script_log(obs.LOG_WARNING, "Tried to save an instant replay, but found no active replay buffer!")
	end
end

----------------------------------------------------------

-- A function named script_update will be called when settings are changed
function script_update(settings)
	source_name = obs.obs_data_get_string(settings, "source")
	source_scene_name = obs.obs_data_get_string(settings, "source_scene")
	source_scene_time = obs.obs_data_get_int(settings, "source_time")
	script_enabled = obs.obs_data_get_bool(settings, "script_enabled")
end

-- A function named script_description returns the description shown to
-- the user
function script_description()
	return "When the \"Instant Replay\" hotkey is triggered, saves a replay with the replay buffer, and then plays it in a media source as soon as the replay is ready.  Requires an active replay buffer.\n\nMade by Jim"
end

-- A function named script_properties defines the properties that the user
-- can change for the entire script module itself
function script_properties()
	props = obs.obs_properties_create()
	
	obs.obs_properties_add_bool(props, "script_enabled", "Enable")
	
	local s = obs.obs_properties_add_list(props, "source_scene", "Replay Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	local scenes = obs.obs_frontend_get_scenes()
	if scenes ~= nil then
		for _, scene in ipairs(scenes) do
			local name = obs.obs_source_get_name(scene)
			obs.obs_property_list_add_string(s, name, name)
		end
	end
	obs.source_list_release(scenes)

	local p = obs.obs_properties_add_list(props, "source", "Media Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	local sources = obs.obs_enum_sources()
	if sources ~= nil then
		for _, source in ipairs(sources) do
			source_id = obs.obs_source_get_id(source)
			if source_id == "ffmpeg_source" then
				local name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)
			end
		end
	end
	obs.source_list_release(sources)
	
	obs.obs_properties_add_int(props, "source_time", "Replay duration (seconds)", 1, 120, 1) 
	
	return props
end

-- A function named script_defaults will be called to set the default settings
function script_defaults(settings)
	obs.obs_data_set_default_int(settings, "source_time", 20)
end

-- A function named script_load will be called on startup
function script_load(settings)
	source_name = obs.obs_data_get_string(settings, "source")
	source_scene_name = obs.obs_data_get_string(settings, "source_scene")
	source_scene_time = obs.obs_data_get_int(settings, "source_time")
	
	show_replay(false)
	hotkey_id = obs.obs_hotkey_register_frontend("obs_instant_replay.trigger", "OBS Instant Replay", obs_instant_replay)
	local hotkey_save_array = obs.obs_data_get_array(settings, "obs_instant_replay.trigger")
	obs.obs_hotkey_load(hotkey_id, hotkey_save_array)
	obs.obs_data_array_release(hotkey_save_array)
end

-- A function named script_save will be called when the script is saved
--
-- NOTE: This function is usually used for saving extra data (such as in this
-- case, a hotkey's save data).  Settings set via the properties are saved
-- automatically.
function script_save(settings)
	local hotkey_save_array = obs.obs_hotkey_save(hotkey_id)
	obs.obs_data_set_array(settings, "obs_instant_replay.trigger", hotkey_save_array)
	obs.obs_data_array_release(hotkey_save_array)
end
