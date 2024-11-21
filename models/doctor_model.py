from app import mongo,bcrypt
from bson import ObjectId
class doctor_model:
    def doctor_signup_model(self,doctor_data):
        try:
            existing_doctor = mongo.db.doctors.find_one({'email': doctor_data['email']})
            if existing_doctor:
                return {'message': 'Email already exists'}
            hashed_password = bcrypt.generate_password_hash(doctor_data['password']).decode('utf-8')
            doctor_data['password'] = hashed_password
            doctor = mongo.db.doctors.insert_one(doctor_data)
            return {'id': str(doctor.inserted_id), 'message': 'ok'}
        except Exception as e:
            return {'message':f"something went wrong{e}"}
    
    def doctor_login_model(self,doctor_data):
        try:
            doctor = mongo.db.doctors.find_one({'email': doctor_data['email']})
            if doctor:
                if bcrypt.check_password_hash(doctor['password'], doctor_data['password']):
                    return {
                        "message": "ok",
                        "doctor": {
                            'id': str(doctor['_id']),
                            'name': doctor['name'],
                            'email': doctor['email'],
                            'specialization':doctor['specialization'],
                            'phone':doctor['phone'],
                            'image':doctor['image'],
                            'status':doctor['status']
                        }
                    }
                return {"message": "Invalid credentials", "user": {}}
            return {"message": "User not found", "user": {}}
        except Exception as e:
            return {'message':f'{e}','user':{}}
    
    def doctor_all_model(self):
        try:
            doctors = list(mongo.db.doctors.find())
            all_docs=[]   
            for doctor in doctors:
                all_docs.append({
                    'id':str(doctor['_id']),
                    'email':doctor['email'],
                    'phone':doctor['phone'],
                    'name':doctor['name'],
                    'specialization':doctor['specialization'],
                    'image':doctor['image'],
                    'status':doctor['status']
                })
            return {"doctors": all_docs,'message':'ok'}
        
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}
    
    def doctor_change_activity_model(self,doctor_data):
        try:
            result=mongo.db.doctors.update_one(
                {'_id':ObjectId(doctor_data['id'])},
                {"$set":{'status':doctor_data['status']}}
            )
            if result.matched_count==0:
                return {'messsage':"doctor not found"}
            return {'message':'ok','status':doctor_data['status']}
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}
        
