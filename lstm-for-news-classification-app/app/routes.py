# coding=utf-8
import os
import time
from flask import Blueprint, render_template, redirect, current_app
from .form_validation import IdentifikasiValidate, IdentifikasiValidateTxt
from .make_predict import MakePredict
from .files_hendler import save_files, delete_file, load_file
from config import Config

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template('home.html', title='Home')

@auth.route('/identification')
def identification():
    return render_template('identifikasi.html', title='Identification')

@auth.route('/summary')
def summary():
    title = 'Model Summary'
    makepredict = MakePredict()
    history = makepredict.history()
    epoch = [e for e in range(0, len(history['accuracy']))]
    return render_template('summary.html', title=title, 
                            acc=history['accuracy'], val_acc=history['val_accuracy'],
                            loss=history['loss'], val_loss=history['val_loss'], epoch=epoch)

@auth.route('/identification/file-predict', methods=['GET','POST'])
def filepredict():
    makepredict = MakePredict()
    predict = makepredict.result
    form = IdentifikasiValidateTxt()
    if form.validate_on_submit():
        file_name = save_files(form.files.data, 'static/file')
        files = load_file(file_name)
        makepredict = MakePredict(files)
        predict = makepredict.filePredict()
        delete_file(file_name, 'static/file')
    return render_template('form1.html', title='Identification', form=form, predict=predict)

@auth.route('/identification/text-predict', methods=['GET','POST'])
def textpredict():
    form = IdentifikasiValidate()
    predict = [0, 0, 0, 0, 0]
    if form.validate_on_submit():
        makepredict = MakePredict(form.article.data)
        predict = makepredict.inputPredict()
        
    return render_template('form2.html', title='Identification', form=form, predict=predict)

# @auth.route('/debag')
# def debag():
#     # path = r"C:\Users\Devone\Desktop\nlp-app\app"
#     # path = r"C:\Users\Devone\Desktop\nlp-app\app"
#     path = os.path.dirname(__file__)
#     # path = os.path.join(current_app.root_path, r'static\file', 'default.jpg')
#     return path