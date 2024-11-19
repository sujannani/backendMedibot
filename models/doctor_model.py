from app import mongo
class doctor_model:
    def doctor_signup_model(self,doctor_data):
        try:
            existing_doctor = mongo.db.doctors.find_one({'email': doctor_data['email']})
            if existing_doctor:
                return {'message': 'Email already exists'}
            doctor=mongo.db.doctors.insert_one(doctor_data)
            return {'id':str(doctor.inserted_id),'message':'ok'}
        except Exception as e:
            return {'message':f"something went wrong{e}"}
    
    def doctor_login_model(self,doctor_data):
        try:
            doctor = mongo.db.users.find_one({'email': doctor_data['email'],'password':doctor_data['password']})
            if doctor:
                return {"message":"ok","user":{
                    'id':str(doctor['_id']),
                    'name':doctor['name'],
                    'email':doctor['email'],
                    'totalAmount':doctor['totalAmount']
                }}
            return {"message":"not ok","user":{}}
        except Exception as e:
            return {'message':f'{e}','user':{}}
    
    def doctor_active_model(self):
        try:
            active_doctors = list(mongo.db.doctors.find({'status': 'active'}))            
            for doctor in active_doctors:
                doctor['_id'] = str(doctor['_id'])            
            return {"doctors": active_doctors,'message':'ok'}
        
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}