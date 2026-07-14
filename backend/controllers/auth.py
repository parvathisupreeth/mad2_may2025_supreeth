from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token

from models import db, User, StudentProfile, CompanyProfile


class LoginResource(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return {
                "message": "Email and Password are required"
            }, 400
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "Invalid Email"}, 401
        if user.password != password:
            return {"message": "Invalid Password"}, 401
        
        access_token = create_access_token(identity=user.email)

        return {
            "message": "Login Successful",
            "access_token": access_token,
            "role": user.role,
            "username": user.username
        }, 200


class RegisterStudentResource(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already exists"}, 400
        user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role="student"
        )

        db.session.add(user)
        db.session.commit()

        student = StudentProfile(
            user_id=user.id,
            name=data["name"],
            branch=data["branch"],
            cgpa=data["cgpa"],
            graduation_year=data["graduation_year"],
            phone=data.get("phone")
        )

        db.session.add(student)
        db.session.commit()

        from tasks import send_welcome_email_task
        send_welcome_email_task.delay(user.email, user.username)

        return {
            "message": "Student Registered Successfully"
        }, 201


class RegisterCompanyResource(Resource):

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No data provided"}, 400
        if User.query.filter_by(email=data["email"]).first():
            return {"message": "Email already exists"}, 400
        user = User(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            role="company"
        )

        db.session.add(user)
        db.session.commit()

        company = CompanyProfile(
            user_id=user.id,
            company_name=data["company_name"],
            hr_name=data["hr_name"],
            hr_email=data["hr_email"],
            website=data.get("website"),
            approval_status="pending"
        )

        db.session.add(company)
        db.session.commit()

        from tasks import send_welcome_email_task
        send_welcome_email_task.delay(user.email, user.username)

        return {
            "message": "Company Registered Successfully. Waiting for Admin Approval."
        }, 201


def register_auth_routes(api):

    api.add_resource(LoginResource,"/login")

    api.add_resource(RegisterStudentResource,"/register/student")

    api.add_resource(RegisterCompanyResource,"/register/company")