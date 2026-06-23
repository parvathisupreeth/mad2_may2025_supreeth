from flask import Flask,request
from models import db,User,StudentProfile,CompanyProfile,PlacementDrive,Application,Interview
from controllers import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
db.init_app(app)

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