import os
import secrets
import pandas as pd
from flask import current_app

def save_files(form_file, path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, path, file_fn)
    form_file.save(file_path)

    return file_fn

def delete_file(file_name, path):
    file_path = os.path.join(current_app.root_path, path, file_name)    
    os.remove(file_path)

def load_file(file_name):
        path = os.path.join(current_app.root_path, 'static/file', file_name)
        files = pd.read_csv(path, header=None, delimiter='\t')
        files.columns = ['category','source', 'article']

        return files