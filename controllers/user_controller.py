# user_controller.py
from app import app
from flask import request  # type: ignore
from models.user_model import user_model

user_obj = user_model()

@app.route('/user/signup', methods=["POST"])
def user_signup_controller():
    return user_obj.user_signup_model(request.form.to_dict())

@app.route('/user/login', methods=["POST"])
def user_login_controller():
    return user_obj.user_login_model(request.form.to_dict())

@app.route('/user/predict',methods=["POST"])
def user_predict_symptom_controller():
    print(request.form.to_dict())
    return user_obj.user_predict_symptom_model(request.form.to_dict())