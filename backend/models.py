from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username=db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False,default='student')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


class StudentProfile(db.Model):
    __tablename__ = "student_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)

    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15))
    resume_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="student_profile")

    def __repr__(self):
        return f"<User {self.username}>"


class CompanyProfile(db.Model):
    __tablename__ = "company_profiles"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,unique=True)

    company_name = db.Column(db.String(150), nullable=False)
    hr_name = db.Column(db.String(100))
    hr_email = db.Column(db.String(120))
    website = db.Column(db.String(255))
    approval_status = db.Column(db.String(20),default="pending")
    is_blacklisted = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    user = db.relationship("User",backref="company_profile")

    def __repr__(self):
        return f"<User {self.username}>"


class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer,db.ForeignKey("company_profiles.id"),nullable=False)

    job_title = db.Column(db.String(150),nullable=False)
    job_description = db.Column(db.Text,nullable=False)
    eligible_branch = db.Column(db.String(100),nullable=False)
    minimum_cgpa = db.Column(db.Float,nullable=False)
    eligible_year = db.Column(db.Integer,nullable=False)
    application_deadline = db.Column(db.Date,nullable=False)
    status = db.Column(db.String(20),default="pending")
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    company = db.relationship("CompanyProfile",backref="placement_drives")

    def __repr__(self):
        return f"<User {self.username}>"


class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey("student_profiles.id"),nullable=False)
    drive_id = db.Column(db.Integer,db.ForeignKey("placement_drives.id"),nullable=False)
    application_date = db.Column(db.DateTime,default=datetime.utcnow)
    status = db.Column(db.String(20),default="applied")
    remarks = db.Column(db.Text)
    student = db.relationship("StudentProfile",backref="applications")
    drive = db.relationship("PlacementDrive",backref="applications")

    def __repr__(self):
        return f"<User {self.username}>"


class Interview(db.Model):
    __tablename__ = "interviews"
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer,db.ForeignKey("applications.id"),nullable=False)
    interview_date = db.Column(db.DateTime,nullable=False)
    meeting_link = db.Column(db.String(255))
    remarks = db.Column(db.Text)
    application = db.relationship("Application",backref="interview")

    def __repr__(self):
        return f"<User {self.username}>"