
import json


def save_progress(user_id, location):
    current_progress = {str(user_id): location}
    try:
        with open('progress.json', 'r') as f:
            progress = json.load(f)
        progress[str(user_id)] = location
        with open('progress.json', 'w') as f:
            json.dump(progress, f)
    except:
        with open('progress.json', 'w') as f:
            json.dump(current_progress, f)


def load_progress(user_id):
    try:
        with open('progress.json', 'r') as f:
            progress = json.load(f)
            return progress.get(str(user_id))
    except FileNotFoundError:
        return None