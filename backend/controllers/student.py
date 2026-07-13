from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from models import db, User, StudentProfile
from flask_restful import Api

# class StudentResource(Resource):

#     @jwt_required()
#     def get(self, student_id=None):
#         ...

#     @jwt_required()
#     def post(self):
#         ...

#     @jwt_required()
#     def put(self, student_id):
#         ...

#     @jwt_required()
#     def delete(self, student_id):
#         ...

# def register_student_routes(api):
#     api.add_resource(
#         StudentResource,
#         "/students",
#         "/students/<int:student_id>"
#     )



class StudentResource(Resource):
    @jwt_required()
    def get (self, student_id=None):
        if student_id:
            student=StudentProfile.query.get(student_id)
            if not student:
                return {"message":f"Student not found"},404
            return{
                "id":student.id,
                "name":student.name,
                "branch":student.branch,
                "cgpa":student.cgpa,
                "graduation_year":student.graduation_year,
                "phone":student.phone,
                "resume_path":student.resume_path},200
        students= StudentProfile.query.all()

        return [{ "id":s.id,
                "name":s.name,
                "branch":s.branch,
                "cgpa":s.cgpa,
                "graduation_year":s.graduation_year
            } for s in students],200
    
    @jwt_required()
    def post (self):
        data=request.get_json()
        if not data:
            return{"message": "no data provided"},400
        user = User.query.get(data["user_id"])
        if not user:
            return {"message":"user not found"},404
        if user.role != "student":
            return {"message": "user is not a student"},400
        
        existing=StudentProfile.query.filter_by(user_id=user.id).first()

        if existing:
            return {"message":"student profile already exists"},400
         
        student=StudentProfile(user_id=data["user_id"],
            name=data["name"],
            branch=data["branch"],
            cgpa=data["cgpa"],
            graduation_year=data["graduation_year"],
            phone=data.get("phone"))
        
        db.session.add(student)
        db.session.commit()
        return {"message": f"posted student info successfully"},201
    
    @jwt_required()
    def put (self, student_id):
        student=StudentProfile.query.get(student_id)
        if not student :
            return {"message":"student not found"},404
        
        data=request.get_json()

        student.name = data.get("name",student.name)
        student.branch=data.get("branch",student.branch)
        student.cgpa=data.get("cgpa",student.cgpa)
        student.graduation_year=data.get("graduation_year",student.graduation_year)
        student.phone=data.get("phone",student.phone)
        student.resume_path=data.get("resume_path",student.resume_path)

        db.session.commit()

        return {"message":f"updated student info succesfully"},200
    
    @jwt_required()
    def delete (self, student_id=None):

        student=StudentProfile.query.get(student_id)
        if not student :
            return {"message": f"student not found"},404
        
        db.session.delete(student)
        db.session.commit()
        return {"message": f"deleted student info successfully"},200

class StudentProfileResource(Resource):
    @jwt_required()
    def get(self):
        from flask_jwt_extended import get_jwt_identity
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()
        if not user or user.role != "student":
            return {"message": "Unauthorized"}, 403
        student = StudentProfile.query.filter_by(user_id=user.id).first()
        if not student:
            return {"message": "Profile not found"}, 404
        return {
            "id": student.id,
            "name": student.name,
            "branch": student.branch,
            "cgpa": student.cgpa,
            "graduation_year": student.graduation_year,
            "phone": student.phone or "",
            "email": user.email
        }, 200

def register_student_routes(api):
    api.add_resource(StudentResource,"/students","/students/<int:student_id>")
    api.add_resource(StudentProfileResource, "/student/profile")
