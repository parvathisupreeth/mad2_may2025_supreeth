from flask import Flask,request
from models import db,User,StudentProfile,CompanyProfile,PlacementDrive,Application,Interview
# from controllers import *
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager

from controllers.auth import register_auth_routes
from controllers.student import register_student_routes
from controllers.company import register_company_routes
from controllers.admin import register_admin_routes
from controllers.application import register_application_routes
from controllers.drive import register_drive_routes

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'


api = Api(app)

register_auth_routes(api)
register_student_routes(api)
register_company_routes(api)
register_admin_routes(api)
register_application_routes(api)
register_drive_routes(api)

db.init_app(app)

app.config['JWT_SECRET_KEY'] = 'your-secret-key' 


jwt = JWTManager(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':

    with app.app_context():
        db.create_all() 
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            admin = User(username='admin',
                         role='admin',
                         email='admin@gmail.com',
                         password='passadmin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin user already exists")

    app.run(debug=True)

