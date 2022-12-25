# coding=utf-8
import os
import joblib
from flask import Flask
from config import Config
from tensorflow.keras.models import load_model


TKNIZER_PATH = "app/models/tokenizers.pkl"
tknizer_open = open(TKNIZER_PATH, 'rb')
tokenizer = joblib.load(tknizer_open)

HISTORY_PATH = "app/models/history91.pkl"
hist_open = open(HISTORY_PATH, 'rb')
history = joblib.load(hist_open)

MODEL_PATH = "app/models/model_lstm.h5"
model = load_model(MODEL_PATH)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes import auth
    app.register_blueprint(auth)

    return app