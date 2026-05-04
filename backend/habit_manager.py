import datetime
import uuid
from . import storage

def get_all_habits() -> list[dict]:
    return storage.load_habits()

def add_habit(name: str) -> None:
    habits = storage.load_habits()
    habit = {
        "id": uuid.uuid4().hex,
        "name": name,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    habits.append(habit)
    storage.save_habits(habits)
    return

def delete_habit(id: str) -> None:
    habits = storage.load_habits()
    habits = [habit for habit in habits if habit["id"] != id]
    storage.save_habits(habits)
    return