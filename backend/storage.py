import json

def load_habits() -> list[dict]:
    habits = []
    try:
        with open("data/habits.json", "r") as f:
            habits = json.load(f)
    except FileNotFoundError:
        with open("data/habits.json", "w") as f:
            json.dump([], f, indent = 4)
    except json.JSONDecodeError:
        # TODO: copy from a backup system inside backups/data/habits.json
        with open("data/habits.json", "w") as f:
            json.dump([], f, indent = 4)
    return habits

def save_habits(data: list[dict]) -> None:
    with open("data/habits.json", "w") as f:
        json.dump(data, f, indent = 4)
    return

def load_logs() -> list[dict]:
    logs = []
    try:
        with open("data/logs.json", "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        with open("data/logs.json", "w") as f:
            json.dump([], f, indent = 4)
    except json.JSONDecodeError:
        # TODO: copy from a backup system inside backups/data/logs.json
        with open("data/logs.json", "w") as f:
            json.dump([], f, indent = 4)
    return logs

def save_logs(data: list[dict]) -> None:
    with open("data/logs.json", "w") as f:
        json.dump(data, f, indent = 4)

def load_settings() -> dict:
    settings = {
    "theme": "light",
    "font_size": "medium",
    "language": "English",
    "week_starts_on": "Monday",
    "reminder_enabled": True,
    "reminder_time": "08:00",
    "weekly_summary": True
    }
    try:
        with open("data/settings.json", "r") as f:
            settings = json.load(f)
    except FileNotFoundError:
        with open("data/settings.json", "w") as f:
            json.dump(settings, f, indent = 4)
    except json.JSONDecodeError:
        # TODO: copy from a backup system inside backups/data/settings.json
        with open("data/settings.json", "w") as f:
            json.dump(settings, f, indent = 4)
    return settings
    
def save_settings(data: dict) -> None:
    with open("data/settings.json", "w") as f:
        json.dump(data, f, indent = 4)