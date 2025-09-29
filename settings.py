import json
import os

CONFIG_FILE = 'config.json'

def load_settings():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {
                    "count_of_drops": 500,
                    "timer_speed": 16,
                    "angle": 5
                }
    else:
        default_settings = {
            "count_of_drops": 500,
            "timer_speed": 16,
            "angle": 5
        }
        save_settings(default_settings)
        return default_settings

def save_settings(settings):

    with open(CONFIG_FILE, 'w') as f:
        json.dump(settings, f, indent=2)