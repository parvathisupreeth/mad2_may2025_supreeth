from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import (  db,User,StudentProfile,CompanyProfile,PlacementDrive,Application,)

class AdminDashboardResource(Resource):

    @jwt_required()
    def get(self):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 404
        if user.role != "admin":
            return {"message": "Unauthorized"}, 403

        return {
            "total_students": StudentProfile.query.count(),
            "total_companies": CompanyProfile.query.count(),
            "total_drives": PlacementDrive.query.count(),
            "total_applications": Application.query.count()
        }, 200
    
class ApproveCompanyResource(Resource):

    @jwt_required()
    def put(self, company_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.get(company_id)

        if not company:
            return {"message": "Company not found"}, 404

        if company.approval_status == "approved":
            return {"message": "Company is already approved"}, 400

        company.approval_status = "approved"

        db.session.commit()

        return {
            "message": f"{company.company_name} approved successfully"
        }, 200
    
class RejectCompanyResource(Resource):

    @jwt_required()
    def put(self, company_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        company = CompanyProfile.query.get(company_id)

        if not company:
            return {"message":"Company not found"},404

        company.approval_status = "rejected"

        db.session.commit()

        return {
            "message": f"{company.company_name} rejected successfully"
        },200
    

class ApproveDriveResource(Resource):

    @jwt_required()
    def put(self, drive_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message":"Placement Drive not found"},404

        if drive.status == "approved":
            return {"message":"Drive already approved"},400

        drive.status = "approved"

        db.session.commit()

        return {
            "message":"Placement Drive approved successfully"
        },200
    

class RejectDriveResource(Resource):

    @jwt_required()
    def put(self, drive_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message":"Placement Drive not found"},404

        drive.status = "rejected"

        db.session.commit()

        return {
            "message":"Placement Drive rejected successfully"
        },200
    

class CompanyListResource(Resource):

    @jwt_required()
    def get(self):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        companies = CompanyProfile.query.all()

        return [{
            "id":company.id,
            "company_name":company.company_name,
            "hr_name":company.hr_name,
            "approval_status":company.approval_status,
            "is_blacklisted":company.is_blacklisted
        } for company in companies],200
    
class StudentListResource(Resource):

    @jwt_required()
    def get(self):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        students = StudentProfile.query.all()

        return [{
            "id":student.id,
            "name":student.name,
            "branch":student.branch,
            "cgpa":student.cgpa,
            "graduation_year":student.graduation_year
        } for student in students],200
    
class BlacklistCompanyResource(Resource):

    @jwt_required()
    def put(self, company_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        company = CompanyProfile.query.get(company_id)

        if not company:
            return {"message":"Company not found"},404

        company.is_blacklisted = True

        db.session.commit()

        return {
            "message":"Company blacklisted successfully"
        },200
    

class DeactivateStudentResource(Resource):

    @jwt_required()
    def put(self, student_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        student = StudentProfile.query.get(student_id)

        if not student:
            return {"message":"Student not found"},404

        student.user.is_active = False

        db.session.commit()

        return {
            "message":"Student deactivated successfully"
        },200


class SearchCompanyResource(Resource):

    @jwt_required()
    def get(self):

        keyword = request.args.get("q")

        companies = CompanyProfile.query.filter(
            CompanyProfile.company_name.ilike(f"%{keyword}%")
        ).all()

        return [{
            "id":company.id,
            "company_name":company.company_name,
            "approval_status":company.approval_status
        } for company in companies],200
    

class SearchStudentResource(Resource):

    @jwt_required()
    def get(self):

        keyword = request.args.get("q")

        students = StudentProfile.query.filter(
            StudentProfile.name.ilike(f"%{keyword}%")
        ).all()

        return [{
            "id":student.id,
            "name":student.name,
            "branch":student.branch,
            "cgpa":student.cgpa
        } for student in students],200
    


    

def register_admin_routes(api):
    api.add_resource(AdminDashboardResource,"/admin/dashboard")

    api.add_resource(ApproveCompanyResource,"/admin/company/<int:company_id>/approve")
    api.add_resource(RejectCompanyResource,"/admin/company/<int:company_id>/reject")

    api.add_resource(ApproveDriveResource,"/admin/drive/<int:drive_id>/approve")
    api.add_resource(RejectDriveResource,"/admin/drive/<int:drive_id>/reject")

    api.add_resource(CompanyListResource,"/admin/companies")
    api.add_resource(StudentListResource,"/admin/students")
    

    api.add_resource(BlacklistCompanyResource,"/admin/company/<int:company_id>/blacklist")
    api.add_resource(DeactivateStudentResource,"/admin/student/<int:student_id>/deactivate")

    api.add_resource(SearchCompanyResource,"/admin/search/company")
    api.add_resource(SearchStudentResource,"/admin/search/student")