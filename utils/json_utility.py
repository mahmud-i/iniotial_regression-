
import json
import utils.json_to_html as ht
from collections import OrderedDict as sort


def save_json(data, file_path):
    try:
        sorted_data = sort(sorted(data.items()))

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")
        ht.generate_html_report(file_path)

    except Exception as e:
        print(f"Error saving Json file: {e}")



def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading Json file: {e}")
        return None