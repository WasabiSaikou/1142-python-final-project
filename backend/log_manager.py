import datetime
from . import storage

def create_log(habit_id: str, date: str) -> None:
    logs = storage.load_logs()
    log = {
        "habit_id": habit_id,
        "date": date,
        "completed": True
    }
    logs.append(log)
    storage.save_logs(logs)
    return

def toggle_check(habit_id: str, date: str) -> bool:
    logs = storage.load_logs()
    matching = [log for log in logs if log["habit_id"] == habit_id and log["date"] == date]
    if matching:
        matching[0]["completed"] = not matching[0]["completed"]
        storage.save_logs(logs)
        return matching[0]["completed"]
    else:
        create_log(habit_id, date)
    return True

def get_today_status(habit_id: str) -> bool | None:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    logs = storage.load_logs()
    matching = [log for log in logs if log["habit_id"] == habit_id and log["date"] == today]
    if matching:
        return matching[0]["completed"]
    return None