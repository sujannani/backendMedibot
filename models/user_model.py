from app import mongo,bcrypt
from bson import ObjectId
from symptom_analyser.app import Symptom_Analyser
class user_model:
    def user_signup_model(self,user_data):
        try:
            existing_user = mongo.db.users.find_one({'email': user_data['email']})
            if existing_user:
                return {'message': 'Email already exists'}
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            user_data['password'] = hashed_password
            user=mongo.db.users.insert_one(user_data)
            return {'id':str(user.inserted_id),'message':'ok'}
        except Exception as e:
            return {'message':f"something went wrong{e}"}
    
    def user_login_model(self,user_data):
        try:
            user = mongo.db.users.find_one({'email': user_data['email']})
            if user:
                if bcrypt.check_password_hash(user['password'], user_data['password']):
                    return {
                        "message": "ok",
                        "user": {
                            'id': str(user['_id']),
                            'name': user['name'],
                            'email': user['email'],
                            'phone':user['phone']
                        }
                    }
                return {"message": "Invalid credentials", "user": {}}
            return {"message":"not ok","user":{}}
        except Exception as e:
            return {'message':f'{e}','user':{}}
    
    def user_predict_symptom_model(self, user_data):
        try:
            sa = Symptom_Analyser()
            symptom = user_data.get('symptom')
            print(symptom)
            if not symptom:
                return {"message": "Symptom is required"},
            disease = sa.predict_disease(symptom)
            return {"prediction": disease,"message":"ok"}
        
        except KeyError as e:
            return {"message": f"Missing key: {str(e)}"}
        except Exception as e:
            return {"message": "An error occurred", "error": str(e)}
        