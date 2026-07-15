import smtplib
import csv
import io
import os
from datetime import date, datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from extensions import celery


def send_email(to_email, subject, body, html_body=None):
    sender = "portal@placement.univ"
    if html_body:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email
        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(html_body, "html"))
    else:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email

    try:
        with smtplib.SMTP('localhost', 1025) as server:
            server.sendmail(sender, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")



@celery.task
def send_welcome_email_task(to_email, username):
    subject = "Welcome to the Placement Portal!"
    body = f"""Hi {username},

Welcome to the Placement Portal! Your account has been successfully registered.

Best regards,
Placement Team"""
    send_email(to_email, subject, body)


@celery.task
def notify_drive_approved_task(to_email, job_title, drive_id):
    subject = f"New Placement Drive: {job_title} Approved!"
    body = f"""Hi Student,

We are happy to inform you that a new placement drive for '{job_title}' has been approved and is open for applications.

Log in to the Placement Portal to view the details and apply before the deadline.

Best regards,
Placement Team"""
    send_email(to_email, subject, body)


@celery.task
def notify_status_change_task(to_email, job_title, status, remarks):
    subject = f"Application Update: {job_title}"
    body = f"""Hi Student,

Your application status for the placement drive '{job_title}' has been updated to: {status}.

Remarks: {remarks or "No remarks provided."}

Best regards,
Placement Team"""
    send_email(to_email, subject, body)


@celery.task
def notify_company_approval_task(to_email, company_name, status):
    if status == "approved":
        subject = f"✅ Your Company '{company_name}' Has Been Approved!"
        body = f"""Hi,

Great news! Your company registration for '{company_name}' on the Placement Portal has been approved by the admin.

You can now log in and start posting placement drives for students.

Best regards,
Placement Portal Team"""
    else:
        subject = f"❌ Your Company '{company_name}' Registration Was Rejected"
        body = f"""Hi,

We regret to inform you that your company registration for '{company_name}' on the Placement Portal has been rejected by the admin.

If you believe this is a mistake, please contact the placement office.

Best regards,
Placement Portal Team"""
    send_email(to_email, subject, body)


@celery.task(name="tasks.send_daily_deadline_reminders")
def send_daily_deadline_reminders():
    """
    Scheduled daily job.
    Notifies students about placement drives whose application
    deadline is within the next 3 days.
    """
    from app import app
    with app.app_context():
        from models import db, User, StudentProfile, Application, PlacementDrive

        today = date.today()
        reminder_window = today + timedelta(days=3)

        upcoming_drives = PlacementDrive.query.filter(
            PlacementDrive.status == "approved",
            PlacementDrive.application_deadline >= today,
            PlacementDrive.application_deadline <= reminder_window
        ).all()

        if not upcoming_drives:
            print("[Daily Reminder] No upcoming deadlines in the next 3 days.")
            return


        drive_ids = [d.id for d in upcoming_drives]
        all_students = StudentProfile.query.all()

        reminders_sent = 0
        for student in all_students:

            applied_drive_ids = {
                app.drive_id for app in
                Application.query.filter(
                    Application.student_id == student.id,
                    Application.drive_id.in_(drive_ids)
                ).all()
            }

            for drive in upcoming_drives:
                if drive.id not in applied_drive_ids:
                    days_left = (drive.application_deadline - today).days
                    subject = f"⏰ Reminder: Apply to '{drive.job_title}' — {days_left} day(s) left!"
                    body = f"""Hi {student.name},

This is a reminder that the application deadline for the following placement drive is approaching:

  🏢 Company : {drive.company.company_name}
  💼 Role    : {drive.job_title}
  📅 Deadline: {drive.application_deadline} ({days_left} day(s) remaining)

Log in to the Placement Portal now to apply before you miss out!

Best regards,
Placement Team"""
                    student_user = User.query.get(student.user_id)
                    if student_user and student_user.is_active:
                        send_email(student_user.email, subject, body)
                        reminders_sent += 1

        print(f"[Daily Reminder] Sent {reminders_sent} reminder email(s).")



@celery.task(name="tasks.send_monthly_report")
def send_monthly_report():
    """
    Scheduled monthly job (runs on the 1st of each month).
    Generates an HTML placement activity report for the previous
    month and emails it to the admin.
    """
    from app import app
    with app.app_context():
        from models import db, User, StudentProfile, CompanyProfile, PlacementDrive, Application
        from sqlalchemy import extract

        today = datetime.utcnow()
        # Report covers the PREVIOUS month
        if today.month == 1:
            report_month = 12
            report_year = today.year - 1
        else:
            report_month = today.month - 1
            report_year = today.year

        month_name = datetime(report_year, report_month, 1).strftime("%B %Y")

        # Stats for the report month
        drives_conducted = PlacementDrive.query.filter(
            extract('month', PlacementDrive.created_at) == report_month,
            extract('year', PlacementDrive.created_at) == report_year
        ).count()

        all_apps_this_month = Application.query.filter(
            extract('month', Application.application_date) == report_month,
            extract('year', Application.application_date) == report_year
        ).all()

        total_applied = len(all_apps_this_month)
        total_selected = sum(1 for a in all_apps_this_month if a.status == "Selected")
        total_rejected = sum(1 for a in all_apps_this_month if a.status == "Rejected")
        total_shortlisted = sum(1 for a in all_apps_this_month if a.status == "Shortlisted")

        total_students = StudentProfile.query.count()
        total_companies = CompanyProfile.query.count()

        # Drive breakdown table rows
        drives_this_month = PlacementDrive.query.filter(
            extract('month', PlacementDrive.created_at) == report_month,
            extract('year', PlacementDrive.created_at) == report_year
        ).all()

        drive_rows = ""
        for drive in drives_this_month:
            applied_count = Application.query.filter_by(drive_id=drive.id).count()
            selected_count = Application.query.filter_by(drive_id=drive.id, status="Selected").count()
            drive_rows += f"""
            <tr>
                <td>{drive.company.company_name}</td>
                <td>{drive.job_title}</td>
                <td style="text-align:center">{applied_count}</td>
                <td style="text-align:center">{selected_count}</td>
                <td style="text-align:center"><span style="color:{'green' if drive.status=='approved' else 'orange'}">{drive.status.capitalize()}</span></td>
            </tr>"""

        html_body = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 20px; }}
  .container {{ max-width: 800px; margin: auto; background: #fff; border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }}
  .header {{ background: linear-gradient(135deg, #1a73e8, #0d47a1); color: white;
             padding: 30px 40px; }}
  .header h1 {{ margin: 0; font-size: 24px; }}
  .header p  {{ margin: 5px 0 0; opacity: 0.85; font-size: 14px; }}
  .content {{ padding: 30px 40px; }}
  .stats-grid {{ display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 24px; }}
  .stat-card {{ flex: 1; min-width: 140px; background: #f0f4ff; border-radius: 8px;
                padding: 16px 20px; text-align: center; }}
  .stat-card .value {{ font-size: 32px; font-weight: bold; color: #1a73e8; }}
  .stat-card .label {{ font-size: 12px; color: #666; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; }}
  th {{ background: #1a73e8; color: white; padding: 10px 12px; text-align: left; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid #e8e8e8; }}
  tr:nth-child(even) td {{ background: #f9f9f9; }}
  .footer {{ background: #f4f6f9; padding: 16px 40px; text-align: center;
             font-size: 12px; color: #999; }}
  h2 {{ color: #1a73e8; border-bottom: 2px solid #e8e8e8; padding-bottom: 8px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📊 Monthly Placement Activity Report</h1>
    <p>Report for: <strong>{month_name}</strong> &nbsp;|&nbsp; Generated on: {today.strftime('%d %b %Y')}</p>
  </div>
  <div class="content">
    <h2>Summary Statistics</h2>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="value">{drives_conducted}</div>
        <div class="label">Drives Conducted</div>
      </div>
      <div class="stat-card">
        <div class="value">{total_applied}</div>
        <div class="label">Students Applied</div>
      </div>
      <div class="stat-card">
        <div class="value">{total_selected}</div>
        <div class="label">Students Selected</div>
      </div>
      <div class="stat-card">
        <div class="value">{total_shortlisted}</div>
        <div class="label">Shortlisted</div>
      </div>
      <div class="stat-card">
        <div class="value">{total_rejected}</div>
        <div class="label">Rejected</div>
      </div>
    </div>

    <h2>Platform Overview</h2>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="value">{total_students}</div>
        <div class="label">Total Students</div>
      </div>
      <div class="stat-card">
        <div class="value">{total_companies}</div>
        <div class="label">Total Companies</div>
      </div>
    </div>

    <h2>Drive-wise Breakdown</h2>
    {'<p style="color:#999">No placement drives were created this month.</p>' if not drives_this_month else f"""
    <table>
      <thead>
        <tr>
          <th>Company</th>
          <th>Job Title</th>
          <th>Applicants</th>
          <th>Selected</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>{drive_rows}</tbody>
    </table>"""}
  </div>
  <div class="footer">
    This is an auto-generated report by the Placement Portal system. &copy; {today.year}
  </div>
</div>
</body>
</html>"""

        plain_body = f"""Monthly Placement Report — {month_name}

Drives Conducted : {drives_conducted}
Students Applied : {total_applied}
Students Selected: {total_selected}
Shortlisted      : {total_shortlisted}
Rejected         : {total_rejected}

Please view the HTML version of this email for the full report.

— Placement Portal System"""

        admin_user = User.query.filter_by(role="admin").first()
        if admin_user:
            send_email(
                admin_user.email,
                f"📊 Monthly Placement Report — {month_name}",
                plain_body,
                html_body=html_body
            )
            print(f"[Monthly Report] Report for {month_name} sent to {admin_user.email}")
        else:
            print("[Monthly Report] No admin user found.")




@celery.task(name="tasks.export_student_applications_csv")
def export_student_applications_csv(student_id, to_email, student_name):
    """
    User-triggered async job.
    Generates a CSV of the student's application history and
    emails it to them as an inline attachment.
    """
    from app import app
    with app.app_context():
        from models import db, StudentProfile, Application, PlacementDrive, CompanyProfile

        applications = Application.query.filter_by(student_id=student_id).all()

        # Build CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Application ID",
            "Student ID",
            "Company Name",
            "Drive Title",
            "Application Status",
            "Application Date",
            "Deadline",
            "Remarks"
        ])

        for app in applications:
            drive = PlacementDrive.query.get(app.drive_id)
            company = CompanyProfile.query.get(drive.company_id) if drive else None
            writer.writerow([
                app.id,
                student_id,
                company.company_name if company else "N/A",
                drive.job_title if drive else "N/A",
                app.status,
                str(app.application_date)[:10],
                str(drive.application_deadline) if drive else "N/A",
                app.remarks or ""
            ])

        csv_content = output.getvalue()
        output.close()

  
        sender = "portal@placement.univ"
        subject = "📄 Your Placement Application History — CSV Export"

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email

        body_text = f"""Hi {student_name},

Your placement application history export is ready!

Please find the CSV data below (also attached as plain text for easy import):

---
{csv_content}
---

This export was generated on {datetime.utcnow().strftime('%d %b %Y at %H:%M UTC')}.

Best regards,
Placement Portal Team"""

        msg.attach(MIMEText(body_text, "plain"))

        from email.mime.base import MIMEBase
        from email import encoders
        attachment = MIMEBase('text', 'csv')
        attachment.set_payload(csv_content.encode('utf-8'))
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            'attachment',
            filename=f"applications_{student_id}_{date.today()}.csv"
        )
        msg.attach(attachment)

        try:
            with smtplib.SMTP('localhost', 1025) as server:
                server.sendmail(sender, [to_email], msg.as_string())
            print(f"[CSV Export] Export emailed to {to_email}")
        except Exception as e:
            print(f"[CSV Export] Failed to send to {to_email}: {e}")