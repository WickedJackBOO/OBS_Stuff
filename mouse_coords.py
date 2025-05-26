"""
mouse position display for obs
this script shows your current mouse position (x and y screen coordinates)
"""

import obspython as obs
import pyautogui

# text source name set by the user
source_name = ""

# on/off switch for updates
enabled = True

# shows up in the script list in obs
def script_description():
    return "shows mouse position (x and y) with a toggle button"

# builds the settings panel for the script
def script_properties():
    props = obs.obs_properties_create()

    # shows helpful instructions
    obs.obs_properties_add_text(props, "info", "info", obs.OBS_TEXT_INFO)
    obs.obs_property_set_long_description(
        obs.obs_properties_get(props, "info"),
        "this script shows your mouse x and y position on screen\n"
        "type in the name of your text source and hit toggle to turn updates on or off"
    )

    # input for the text source name
    obs.obs_properties_add_text(props, "source_name", "Text Source Name", obs.OBS_TEXT_DEFAULT)

    # button to turn updates on or off
    obs.obs_properties_add_button(props, "toggle_button", "Toggle On/Off", toggle_button_pressed)

    return props

# updates when settings are changed
def script_update(settings):
    global source_name

    source_name = obs.obs_data_get_string(settings, "source_name")

    # start or restart the timer to call update_text
    obs.timer_remove(update_text)
    obs.timer_add(update_text, 50)  # every 50ms

    # obs.script_log(obs.LOG_INFO, f"[debug] updates linked to source: {source_name}")

# runs when the toggle button is clicked
def toggle_button_pressed(props, prop):
    global enabled
    enabled = not enabled
    state = "ON" if enabled else "OFF"
    # obs.script_log(obs.LOG_INFO, f"[debug] updates toggled: {state}")

# this runs on a loop every 50ms
def update_text():
    global source_name, enabled

    # skip updates if toggle is off
    if not enabled:
        return

    # get current mouse position
    x, y = pyautogui.position()

    # build the string to show
    text = f"X: {x}\nY: {y}"

    # find the text source by name
    source = obs.obs_get_source_by_name(source_name)
    if not source:
        # obs.script_log(obs.LOG_WARNING, f"[debug] source '{source_name}' not found")
        return

    # update the text on screen
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, "text", text)
    obs.obs_source_update(source, settings)

    # clean up
    obs.obs_data_release(settings)
    obs.obs_source_release(source)
