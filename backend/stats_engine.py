from datetime import datetime, timedelta
from . import habit_manager, log_manager

def get_prev_date(date:str) -> str:
    curr = datetime.strptime(date, "%Y-%m-%d")
    prev = curr - timedelta(days = 1)
    return prev.strftime("%Y-%m-%d")

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

def get_longest_streak(habit_id:str) -> int:
    longest_streak = 0
    curr_streak = 0
    habits = habit_manager.get_all_habits()
    habit = [habit for habit in habits if habit["id"] == habit_id]
    created_at = habit[0]["created_at"]
    
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
    