import json
import os

def config():
    file_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f'{file_dir}/conf.json', 'r') as f:
        data = json.load(f)
        return data