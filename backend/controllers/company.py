from flask_restful import Resource,request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import (db,User,CompanyProfile,PlacementDrive)


class CompanyProfileResource(Resource):

    @jwt_required()
    def get(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 404
        if user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        if not company:
            return {"message": "Company profile not found"}, 404

        return {
            "id": company.id,
            "company_name": company.company_name,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "website": company.website,
            "approval_status": company.approval_status,
            "is_blacklisted": company.is_blacklisted
        }, 200
    

class CreatePlacementDriveResource(Resource):

    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user:
            return {"message": "User not found"}, 404
        if user.role != "company":
            return {"message": "Unauthorized"}, 403
        
        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        if not company:
            return {"message": "Company profile not found"}, 404
        if company.approval_status != "approved":
            return {
                "message": "Company is waiting for admin approval."
            }, 403
        if company.is_blacklisted:
            return {
                "message": "Company has been blacklisted."
            }, 403
        
        data = request.get_json()

        drive = PlacementDrive(
            company_id=company.id,
            job_title=data["job_title"],
            job_description=data["job_description"],
            eligible_branch=data["eligible_branch"],
            minimum_cgpa=data["minimum_cgpa"],
            eligible_year=data["eligible_year"],
            application_deadline=data["application_deadline"],
            status="pending"
        )

        db.session.add(drive)
        db.session.commit()

        return {
            "message": "Placement Drive created successfully and sent for Admin Approval."
        }, 201
    

class CompanyDrivesResource(Resource):

    @jwt_required()
    def get(self):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()

        if not company:
            return {"message": "Company not found"}, 404

        drives = PlacementDrive.query.filter_by(company_id=company.id).all()

        return [{
            "id": drive.id,
            "job_title": drive.job_title,
            "eligible_branch": drive.eligible_branch,
            "minimum_cgpa": drive.minimum_cgpa,
            "eligible_year": drive.eligible_year,
            "application_deadline": str(drive.application_deadline),
            "status": drive.status
        } for drive in drives], 200
    
class UpdatePlacementDriveResource(Resource):

    @jwt_required()
    def put(self, drive_id):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message": "Drive not found"}, 404
        if drive.company_id != company.id:
            return {"message": "Permission denied"}, 403

        data = request.get_json()

        drive.job_title = data.get("job_title", drive.job_title)
        drive.job_description = data.get("job_description", drive.job_description)
        drive.eligible_branch = data.get("eligible_branch", drive.eligible_branch)
        drive.minimum_cgpa = data.get("minimum_cgpa", drive.minimum_cgpa)
        drive.eligible_year = data.get("eligible_year", drive.eligible_year)
        drive.application_deadline = data.get(
            "application_deadline",
            drive.application_deadline
        )

        db.session.commit()
        return {"message": "Placement Drive updated successfully"}, 200
    
class DeletePlacementDriveResource(Resource):

    @jwt_required()
    def delete(self, drive_id):

        email = get_jwt_identity()
        user = User.query.filter_by(email=email).first()

        if not user or user.role != "company":
            return {"message": "Unauthorized"}, 403

        company = CompanyProfile.query.filter_by(user_id=user.id).first()
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message": "Drive not found"}, 404
        if drive.company_id != company.id:
            return {"message": "Permission denied"}, 403

        db.session.delete(drive)
        db.session.commit()

        return {"message": "Placement Drive deleted successfully"}, 200
    
def register_company_routes(api):

    api.add_resource(CompanyProfileResource,"/company/profile")
    
    api.add_resource(CreatePlacementDriveResource,"/company/drive")
    api.add_resource(CompanyDrivesResource,"/company/drives")
    api.add_resource(UpdatePlacementDriveResource,"/company/drive/<int:drive_id>")
    api.add_resource(DeletePlacementDriveResource,"/company/drive/<int:drive_id>")