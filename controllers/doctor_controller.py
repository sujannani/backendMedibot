# user_controller.py
from app import app
from flask import request  # type: ignore
from models.doctor_model import doctor_model

doctor_obj = doctor_model()

@app.route('/doctor/signup', methods=["POST"])
def doctor_signup_controller():
    return doctor_obj.doctor_signup_model(request.form.to_dict())

@app.route('/doctor/login', methods=["POST"])
def doctor_login_controller():
    return doctor_obj.doctor_login_model(request.form.to_dict())

@app.route('/doctor/all-doctors')
def doctor_all_controller():
    return doctor_obj.doctor_all_model()

@app.route('/doctor/change-activity',methods=["POST"])
def doctor_change_activity_controller():
    return doctor_obj.doctor_change_activity_model(request.form.to_dict())