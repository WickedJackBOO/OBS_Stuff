"""
mouse delta display for obs
this script shows how much your mouse moves each frame (x and y change)
you choose the fps so it matches your recording speed (like 60 fps)
"""

import obspython as obs
import pyautogui

# user input values
sourceName = ""
userFps = 60

# stores last known mouse position
lastX = None
lastY = None

# toggle state (on/off)
enabled = True

# description that shows up in the script list
def script_description():
    return "shows mouse movement (x and y) for each frame"

# settings menu in obs
def script_properties():
    props = obs.obs_properties_create()

    # shows a quick description label in the panel
    obs.obs_properties_add_text(props, "info", "info", obs.OBS_TEXT_INFO)
    obs.obs_property_set_long_description(
        obs.obs_properties_get(props, "info"),
        "this script tracks how much the mouse moves per frame\n"
        "type your text source name and set your current recording fps (default is set to 60)\n"
        "then hit the toggle button to turn updates on or off"
    )

    # text source name input
    obs.obs_properties_add_text(props, "sourceName", "Text Source Name", obs.OBS_TEXT_DEFAULT)

    # user chooses fps (updates per second)
    obs.obs_properties_add_int(props, "userFps", "Frames Per Second", 1, 240, 1)

    # toggle button to turn tracking on/off
    obs.obs_properties_add_button(props, "toggle_button", "Toggle On/Off", toggle_button_pressed)

    return props

# updates when user changes input settings
def script_update(settings):
    global sourceName, userFps

    # get input values from the settings panel
    sourceName = obs.obs_data_get_string(settings, "sourceName")
    userFps = obs.obs_data_get_int(settings, "userFps")

    if userFps <= 0:
        userFps = 60  # use default if bad input

    intervalMs = int(1000 / userFps)

    # restart the update timer
    obs.timer_remove(update_text)
    obs.timer_add(update_text, intervalMs)

    # obs.script_log(obs.LOG_INFO, f"[debug] fps set to {userFps}, update interval {intervalMs}ms")
    # obs.script_log(obs.LOG_INFO, f"[debug] source set to '{sourceName}'")

# this runs every time the toggle button is clicked
def toggle_button_pressed(props, prop):
    global enabled
    enabled = not enabled
    state = "ON" if enabled else "OFF"
    # obs.script_log(obs.LOG_INFO, f"[debug] updates toggled: {state}")

# this runs on every timer update
def update_text():
    global sourceName, lastX, lastY, enabled

    # skip if toggle is off
    if not enabled:
        return

    # get current mouse position
    x, y = pyautogui.position()

    # setup last position on first run
    if lastX is None or lastY is None:
        lastX = x
        lastY = y
        return

    # calculate movement (delta)
    moveX = x - lastX
    moveY = y - lastY

    # save current position
    lastX = x
    lastY = y

    # create text output
    text = f"X: {moveX:+}\nY: {moveY:+}"

    # find the obs text source and update it
    source = obs.obs_get_source_by_name(sourceName)
    if not source:
        obs.script_log(obs.LOG_WARNING, f"[debug] source '{sourceName}' not found")
        return

    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", text)
    obs.obs_source_update(source, settings)

    obs.obs_data_release(settings)
    obs.obs_source_release(source)
