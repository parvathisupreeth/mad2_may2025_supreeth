from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date

from models import (db,User,StudentProfile,CompanyProfile,PlacementDrive,Application)


class ApplyDriveResource(Resource):

    @jwt_required()
    def post(self, drive_id):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "student":
            return {"message":"Unauthorized"},403
        
        student = StudentProfile.query.filter_by(user_id=user.id).first()

        if not student:
            return {"message":"Student profile not found"},404

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message":"Placement Drive not found"},404
        
        if drive.status != "approved":
            return {"message":"Drive is not approved yet."},400

        if drive.application_deadline < date.today():
            return {"message":"Application deadline has passed."},400

        eligible_branches = [b.strip() for b in drive.eligible_branch.split(",")]
        if student.branch not in eligible_branches:
            return {"message": "Branch not eligible."}, 400

        if student.cgpa < drive.minimum_cgpa:
            return {"message":"CGPA not eligible."},400

        if student.graduation_year != drive.eligible_year:return {"message":"Graduation year not eligible."},400

        existing = Application.query.filter_by(student_id=student.id,drive_id=drive.id).first()
        if existing:return {"message":"Already applied."},400

        application = Application(student_id=student.id,drive_id=drive.id)
        db.session.add(application)
        db.session.commit()

        return {"message":"Application submitted successfully."},201
    



class StudentApplicationHistoryResource(Resource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "student":
            return {"message": "Unauthorized"}, 403

        student = StudentProfile.query.filter_by(user_id=user.id).first()

        if not student:
            return {"message": "Student profile not found"}, 404
        applications = Application.query.filter_by(student_id=student.id).all()

        result = []

        for app in applications:
            drive = PlacementDrive.query.get(app.drive_id)
            company = CompanyProfile.query.get(drive.company_id)

            result.append({
                "application_id": app.id,
                "drive_id": app.drive_id,
                "company_name": company.company_name,
                "job_title": drive.job_title,
                "application_date": str(app.application_date),
                "status": app.status,
                "remarks": app.remarks
            })

        return result, 200
    
    
class CompanyApplicantsResource(Resource):

    @jwt_required()
    def get(self, drive_id):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message": "Placement Drive not found"}, 404
        if drive.company_id != company.id:
            return {"message": "Permission denied"}, 403
        applications = Application.query.filter_by(drive_id=drive.id).all()

        result = []

        for app in applications:
            student = StudentProfile.query.get(app.student_id)

            result.append({
                "application_id": app.id,
                "student_name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "graduation_year": student.graduation_year,
                "resume_path": student.resume_path,
                "status": app.status,
                "remarks": app.remarks
            })

        return result, 200
    

class UpdateApplicationStatusResource(Resource):

    @jwt_required()
    def put(self, application_id):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        application = Application.query.get(application_id)

        if not application:
            return {"message": "Application not found"}, 404

        drive = PlacementDrive.query.get(application.drive_id)

        if drive.company_id != company.id:
            return {"message": "Permission denied"}, 403

        data = request.get_json()
        status = data.get("status")
        remarks = data.get("remarks")
        allowed_status = ["applied","Shortlisted","Selected","Rejected"]

        if status not in allowed_status:
            return {"message": "Invalid status"}, 400

        application.status = status
        application.remarks = remarks
        db.session.commit()

        return {"message": "Application updated successfully"}, 200


class CompanyAllApplicationsResource(Resource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        if not company:
            return {"message": "Company not found"}, 404

        search = request.args.get("search", "").strip().lower()

        drives = PlacementDrive.query.filter_by(company_id=company.id).all()
        result = []

        for drive in drives:
            applications = Application.query.filter_by(drive_id=drive.id).all()
            for app in applications:
                student = StudentProfile.query.get(app.student_id)
                if search and search not in student.name.lower():
                    continue
                result.append({
                    "application_id": app.id,
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "student_name": student.name,
                    "branch": student.branch,
                    "cgpa": student.cgpa,
                    "graduation_year": student.graduation_year,
                    "resume_path": student.resume_path,
                    "application_date": str(app.application_date)[:10],
                    "status": app.status,
                    "remarks": app.remarks or ""
                })

        return result, 200


def register_application_routes(api):
    api.add_resource(ApplyDriveResource,"/student/apply/<int:drive_id>")
    api.add_resource(StudentApplicationHistoryResource,"/student/applications")
    api.add_resource(CompanyApplicantsResource,"/company/applicants/<int:drive_id>")
    api.add_resource(UpdateApplicationStatusResource,"/company/application/<int:application_id>/status")
    api.add_resource(CompanyAllApplicationsResource,"/company/applications")