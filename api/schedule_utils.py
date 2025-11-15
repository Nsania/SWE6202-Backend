import pandas as pd
import os
from django.conf import settings
from django.core.cache import cache

SCHEDULE_FILE_PATH = os.path.join(settings.BASE_DIR, 'schedules.csv')
SCHEDULE_CACHE_KEY = 'schedules_data'

def _load_and_cache_schedules():
    
    try:
        df = pd.read_csv(SCHEDULE_FILE_PATH, dtype=str)
        
        schedules_dict = {}
        for index, row in df.iterrows():
            days_list = []
            if pd.notna(row['days']):
                days_list = [day.strip() for day in row['days'].split('|')]
            
            schedules_dict[row['schedule_id']] = {
                'course': row['course'],
                'year': row['year'],
                'days_list': days_list
            }
        
        cache.set(SCHEDULE_CACHE_KEY, schedules_dict, 3600)
        return schedules_dict
        
    except FileNotFoundError:
        raise Exception(f"Configuration Error: 'schedules.csv' not found at {SCHEDULE_FILE_PATH}")
    except Exception as e:
        raise Exception(f"Data Processing Error in schedules.csv: {str(e)}")

def get_all_schedules():
    schedules = cache.get(SCHEDULE_CACHE_KEY)
    if not schedules:
        schedules = _load_and_cache_schedules()
    return schedules

def get_student_schedule_by_id(schedule_id):
    if not schedule_id:
        return {"error": "Student has no schedule_id assigned."}
        
    all_schedules = get_all_schedules()
    
    schedule_data = all_schedules.get(str(schedule_id))
    
    if not schedule_data:
        raise Exception(f"Schedule ID '{schedule_id}' not found in schedules.csv.")
    
    return schedule_data