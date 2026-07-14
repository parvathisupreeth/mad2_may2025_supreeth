from flask_restful import Resource, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache_config import cache

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

        # Calculations for pie chart
        total_students = StudentProfile.query.count()
        
        all_apps = Application.query.all()
        applied_student_ids = {a.student_id for a in all_apps}
        not_applied = total_students - len(applied_student_ids)
        
        placed_apps = Application.query.filter(Application.status.ilike('Selected')).all()
        placed_student_ids = {a.student_id for a in placed_apps}
        placed = len(placed_student_ids)
        
        rejected_apps = Application.query.filter(Application.status.ilike('Rejected')).all()
        rejected_student_ids = {a.student_id for a in rejected_apps}
        rejected = len(rejected_student_ids - placed_student_ids)
        
        other = len(applied_student_ids - placed_student_ids - rejected_student_ids)

        from datetime import datetime
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        drives_this_month = PlacementDrive.query.filter(
            db.extract('month', PlacementDrive.created_at) == current_month,
            db.extract('year', PlacementDrive.created_at) == current_year
        ).count()

        # Count drives per month for the current year
        from sqlalchemy import func
        drives_by_month = db.session.query(
            db.extract('month', PlacementDrive.created_at).label('month'),
            func.count(PlacementDrive.id).label('count')
        ).filter(
            db.extract('year', PlacementDrive.created_at) == current_year
        ).group_by(
            db.extract('month', PlacementDrive.created_at)
        ).all()

        monthly_drives_data = [0] * 12
        for row in drives_by_month:
            m = row[0]
            c = row[1]
            if m and 1 <= int(m) <= 12:
                monthly_drives_data[int(m) - 1] = c

        from extensions import cache
        cache_key = "admin_dashboard_stats"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200

        result = {
            "total_students": total_students,
            "total_companies": CompanyProfile.query.count(),
            "total_drives": PlacementDrive.query.count(),
            "total_applications": len(all_apps),
            "pie_chart": {
                "placed": placed,
                "rejected": rejected,
                "not_applied": not_applied,
                "other": other
            },
            "drives_this_month": drives_this_month,
            "monthly_drives": monthly_drives_data
        }
        cache.set(cache_key, result, timeout=60)
        return result, 200
    
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

        from extensions import cache
        cache.delete("admin_dashboard_stats")

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

        from extensions import cache
        cache.delete("admin_dashboard_stats")

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

       
        from extensions import cache
        cache.delete("admin_dashboard_stats")
        cache.delete("student_eligible_drives")
        cache.delete(f"company_dashboard_stats_{drive.company_id}")

        # Send notifications asynchronously via Celery
        from tasks import notify_drive_approved_task
        students = User.query.filter_by(role="student").all()
        for s in students:
            notify_drive_approved_task.delay(s.email, drive.job_title, drive.id)

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

        from extensions import cache
        cache.delete("admin_dashboard_stats")
        cache.delete("student_eligible_drives")
        cache.delete(f"company_dashboard_stats_{drive.company_id}")

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
            "email":company.user.email,
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
            "graduation_year":student.graduation_year,
            "is_active":student.user.is_active
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

        from extensions import cache
        cache.delete("admin_dashboard_stats")

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

        from extensions import cache
        cache.delete("admin_dashboard_stats")

        return {
            "message":"Student deactivated successfully"
        },200


class ActivateStudentResource(Resource):

    @jwt_required()
    def put(self, student_id):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        student = StudentProfile.query.get(student_id)

        if not student:
            return {"message":"Student not found"},404

        student.user.is_active = True

        db.session.commit()

        from extensions import cache
        cache.delete("admin_dashboard_stats")

        return {
            "message":"Student activated successfully"
        },200


class DriveListResource(Resource):

    @jwt_required()
    def get(self):

        email = get_jwt_identity()

        user = User.query.filter_by(email=email).first()

        if not user or user.role != "admin":
            return {"message":"Unauthorized"},403

        drives = PlacementDrive.query.all()

        return [{
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "eligible_branch": drive.eligible_branch,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_year": drive.eligible_year,
            "application_deadline": str(drive.application_deadline),
            "status": drive.status
        } for drive in drives], 200


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
    api.add_resource(DriveListResource,"/admin/drives")
    

    api.add_resource(BlacklistCompanyResource,"/admin/company/<int:company_id>/blacklist")
    api.add_resource(DeactivateStudentResource,"/admin/student/<int:student_id>/deactivate")
    api.add_resource(ActivateStudentResource,"/admin/student/<int:student_id>/activate")

    api.add_resource(SearchCompanyResource,"/admin/search/company")
    api.add_resource(SearchStudentResource,"/admin/search/student")