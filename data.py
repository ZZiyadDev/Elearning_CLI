import json
import os

def load_data(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_next_id(data_list):
    if not data_list:
        return 1
    return max(item.get('id', 0) for item in data_list) + 1

# Specific helpers

def load_users():
    return load_data('users.json')

def save_users(users):
    save_data('users.json', users)

def load_courses():
    return load_data('courses.json')

def save_courses(courses):
    save_data('courses.json', courses)

def load_progress():
    return load_data('progress.json')

def save_progress(progress):
    save_data('progress.json', progress)
