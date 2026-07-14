from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models import PlacementDrive, CompanyProfile


class AllDrivesResource(Resource):

    @jwt_required()
    def get(self):
        from extensions import cache
        cache_key = "student_eligible_drives"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200

        drives = PlacementDrive.query.filter_by(status="approved").all()
        result = []
        for drive in drives:
            company = CompanyProfile.query.get(drive.company_id)
            result.append({
                "drive_id": drive.id,
                "company_name": company.company_name,
                "job_title": drive.job_title,
                "job_description": drive.job_description,
                "eligible_branch": drive.eligible_branch,
                "minimum_cgpa": drive.minimum_cgpa,
                "eligible_year": drive.eligible_year,
                "application_deadline": str(drive.application_deadline)
            })
            
        cache.set(cache_key, result, timeout=60)
        return result,200
    

class DriveDetailsResource(Resource):

    @jwt_required()
    def get(self, drive_id):
        drive = PlacementDrive.query.get(drive_id)

        if not drive:
            return {"message":"Drive not found"},404

        company = CompanyProfile.query.get(drive.company_id)

        return {
            "drive_id":drive.id,
            "company_name":company.company_name,
            "job_title":drive.job_title,
            "job_description":drive.job_description,
            "eligible_branch":drive.eligible_branch,
            "minimum_cgpa":drive.minimum_cgpa,
            "eligible_year":drive.eligible_year,
            "application_deadline":str(drive.application_deadline),
            "status":drive.status
        },200
    

def register_drive_routes(api):

    api.add_resource(AllDrivesResource,"/drives")
    api.add_resource(DriveDetailsResource,"/drives/<int:drive_id>")