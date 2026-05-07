import json
import calendar
from datetime import datetime, timedelta
from . import habit_manager, log_manager, storage

def get_week_range(date: str) -> dict[str: str]:
    settings = storage.load_settings()
    curr = datetime.strptime(date, "%Y-%m-%d")
    if settings["week_starts_on"] == "Monday":
        start = curr - timedelta(days = curr.weekday())
    else:
        if curr.weekday() == 6:
            start = curr
        else:
            start = curr - timedelta(days = curr.weekday() + 1)
    end = start + timedelta(days = 6)
    return {"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d")}

def get_month_range(date: str) -> dict[str: str]:
    start = date[:-2] + "01"
    first_weekday, num_days = calendar.monthrange(int(start[0:4]), int(start[5:7]))
    end = date[:-2] + str(num_days)
    return {"start": start, "end": end}

def get_prev_date(date: str) -> str:
    curr = datetime.strptime(date, "%Y-%m-%d")
    prev = curr - timedelta(days = 1)
    return prev.strftime("%Y-%m-%d")

def get_next_date(date: str) -> str:
    curr = datetime.strptime(date, "%Y-%m-%d")
    next = curr + timedelta(days = 1)
    return next.strftime("%Y-%m-%d")

def get_create_date(habit_id: str) -> str:
    habits = habit_manager.get_all_habits()
    habit = [habit for habit in habits if habit["id"] == habit_id]
    return habit[0]["created_at"]
    
def check_date_in_habit(habit_id: str, date: str) -> bool:
    created_at = get_create_date(habit_id)
    today = datetime.now().strftime("%Y-%m-%d")
    return created_at <= date <= today

def get_current_streak(habit_id: str) -> int:
    streak = 0
    curr = datetime.now().strftime("%Y-%m-%d")
    
    if log_manager.get_status(habit_id, curr) == True:
        streak += 1
        
    prev = get_prev_date(curr)
    while log_manager.get_status(habit_id, prev) == True:
        streak += 1
        curr = prev
        prev = get_prev_date(curr)
        
    return streak

def get_longest_streak(habit_id: str) -> int:
    longest_streak = 0
    curr_streak = 0
    created_at = get_create_date(habit_id)
    
    curr = datetime.now().strftime("%Y-%m-%d")
    
    if log_manager.get_status(habit_id, curr) == True:
        curr_streak = 1
        longest_streak = 1
        
    if curr == created_at:
        return curr_streak
    
    prev = get_prev_date(curr) 
    while prev != get_prev_date(created_at):
        if log_manager.get_status(habit_id, prev) == True:
            curr_streak += 1
        else:
            curr_streak = 0
        if curr_streak > longest_streak:
            longest_streak = curr_streak
        curr = prev
        prev = get_prev_date(curr)
    
    return longest_streak

def get_range_status(habit_id: str, from_date: str, to_date: str) -> list[bool | None]:
    statuses = []
    curr = from_date
    while curr != get_next_date(to_date):
        if not check_date_in_habit(habit_id, curr):
            statuses.append(None)
            curr = get_next_date(curr)
            continue
        status = log_manager.get_status(habit_id, curr)
        if status == None:
            statuses.append(False)
        else:
            statuses.append(status)
        curr = get_next_date(curr)
    return statuses
    
def get_range_rate(habit_id: str, from_date: str, to_date: str) -> float:
    total = 0
    completed = 0
    statuses = get_range_status(habit_id, from_date, to_date)
    for status in statuses:
        if status == None:
            continue
        if status == True:
            completed += 1
        total += 1
    if total == 0:
        return 0.0
    return completed / total
    
def get_cumulative_rate(habit_id: str, from_date: str, to_date:str) -> list[float]:
    statuses = get_range_status(habit_id, from_date, to_date)
    rates = []
    curr = from_date
    total = 0
    completed = 0
    for status in statuses:
        if status == None:
            rates.append(0.0)
            continue
        if status == True:
            completed += 1
        total += 1
        rates.append(completed / total)
    return rates
