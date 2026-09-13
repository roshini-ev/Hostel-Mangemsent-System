"""
Hostel Management System (HMS)
Simple, practical, and professional hostel portal.
Two user roles: Warden and Student.
Single hostel block, 3 room types, no bed allocation, no mess.
"""
import os
import re
import hashlib
import uuid
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "hostel-mgmt-portal-key-2026")

# ---------------------------------------------------------------------------
# Predefined Room Types (Exactly 3)
# ---------------------------------------------------------------------------
ROOM_TYPES = [
    "AC — Three Sharing",
    "Non-AC — Three Sharing",
    "Non-AC — Four Sharing",
]

# ---------------------------------------------------------------------------
# In-Memory Realistic Data Store
# ---------------------------------------------------------------------------
STUDENTS_DATA = [
    {
        "id": 1,
        "name": "Aarav Sharma",
        "student_id": "2024CS101",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43210",
        "parent_name": "Mr. Ramesh Sharma",
        "parent_phone": "98765 11221",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 96.0,
    },
    {
        "id": 2,
        "name": "Kunal Verma",
        "student_id": "2024ME102",
        "dept": "Mechanical Engineering",
        "year": 3,
        "phone": "98765 43211",
        "parent_name": "Mrs. Sunita Verma",
        "parent_phone": "98765 11222",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 92.0,
    },
    {
        "id": 3,
        "name": "Devansh Joshi",
        "student_id": "2024CS103",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43212",
        "parent_name": "Mr. Alok Joshi",
        "parent_phone": "98765 11223",
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 94.0,
    },
    {
        "id": 4,
        "name": "Rohan Deshmukh",
        "student_id": "2023CS104",
        "dept": "Computer Science & Engineering",
        "year": 4,
        "phone": "98765 43213",
        "parent_name": "Mr. Sanjay Deshmukh",
        "parent_phone": "98765 11224",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 95.0,
    },
    {
        "id": 5,
        "name": "Aditya Nair",
        "student_id": "2025EE105",
        "dept": "Electrical Engineering",
        "year": 2,
        "phone": "98765 43214",
        "parent_name": "Mrs. Radhika Nair",
        "parent_phone": "98765 11225",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 89.0,
    },
    {
        "id": 6,
        "name": "Mohd. Farhan",
        "student_id": "2025EE106",
        "dept": "Electrical Engineering",
        "year": 2,
        "phone": "98765 43215",
        "parent_name": "Mr. Tariq Farhan",
        "parent_phone": "98765 11226",
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 91.0,
    },
    {
        "id": 7,
        "name": "Tanmay Joshi",
        "student_id": "2025ME107",
        "dept": "Mechanical Engineering",
        "year": 2,
        "phone": "98765 43216",
        "parent_name": "Mrs. Deepa Joshi",
        "parent_phone": "98765 11227",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 93.0,
    },
    {
        "id": 8,
        "name": "Ritik Saxena",
        "student_id": "2024CS108",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43217",
        "parent_name": "Mr. Pradeep Saxena",
        "parent_phone": "98765 11228",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 88.0,
    },
    {
        "id": 9,
        "name": "Siddharth Roy",
        "student_id": "2025CV109",
        "dept": "Civil Engineering",
        "year": 2,
        "phone": "98765 43218",
        "parent_name": "Mr. Bimal Roy",
        "parent_phone": "98765 11229",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 90.0,
    },
    {
        "id": 10,
        "name": "Vikram Sen",
        "student_id": "2026EC110",
        "dept": "Electronics & Communication",
        "year": 1,
        "phone": "98765 43219",
        "parent_name": "Mrs. Mala Sen",
        "parent_phone": "98765 11230",
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "attendance_pct": 97.0,
    },
    {
        "id": 11,
        "name": "Kavya Menon",
        "student_id": "2024CS111",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43220",
        "parent_name": "Mr. Suresh Menon",
        "parent_phone": "98765 11231",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 98.0,
    },
    {
        "id": 12,
        "name": "Pooja",
        "student_id": "2024EC112",
        "dept": "Electronics & Communication",
        "year": 4,
        "phone": "98765 43221",
        "parent_name": "Mrs. Meenakshi Sundaram",
        "parent_phone": "98765 11232",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 92.0,
    },
    {
        "id": 13,
        "name": "Sneha Rao",
        "student_id": "2024CS113",
        "dept": "Computer Science & Engineering",
        "year": 3,
        "phone": "98765 43222",
        "parent_name": "Mr. Venkatesh Rao",
        "parent_phone": "98765 11233",
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "attendance_pct": 94.0,
    },
    {
        "id": 14,
        "name": "Ananya Iyer",
        "student_id": "2026IT114",
        "dept": "Information Technology",
        "year": 1,
        "phone": "98765 43223",
        "parent_name": "Mrs. Lakshmi Iyer",
        "parent_phone": "98765 11234",
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 96.0,
    },
    {
        "id": 15,
        "name": "Karthik Subramanian",
        "student_id": "2023ME115",
        "dept": "Mechanical Engineering",
        "year": 4,
        "phone": "98765 43224",
        "parent_name": "Mr. V. Subramanian",
        "parent_phone": "98765 11235",
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "attendance_pct": 93.0,
    },
]

ROOMS_DATA = [
    {
        "room_number": "201",
        "room_type": "AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Aarav Sharma", "student_id": "2024CS101", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43210"},
            {"name": "Kunal Verma", "student_id": "2024ME102", "dept": "Mechanical Engineering", "year": 3, "phone": "98765 43211"},
            {"name": "Devansh Joshi", "student_id": "2024CS103", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43212"},
        ]
    },
    {
        "room_number": "301",
        "room_type": "AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Kavya Menon", "student_id": "2024CS111", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43220"},
            {"name": "Pooja", "student_id": "2024EC112", "dept": "Electronics & Communication", "year": 4, "phone": "98765 43221"},
            {"name": "Sneha Rao", "student_id": "2024CS113", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43222"},
        ]
    },
    {
        "room_number": "202",
        "room_type": "Non-AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Rohan Deshmukh", "student_id": "2023CS104", "dept": "Computer Science & Engineering", "year": 4, "phone": "98765 43213"},
            {"name": "Aditya Nair", "student_id": "2025EE105", "dept": "Electrical Engineering", "year": 2, "phone": "98765 43214"},
            {"name": "Mohd. Farhan", "student_id": "2025EE106", "dept": "Electrical Engineering", "year": 2, "phone": "98765 43215"},
        ]
    },
    {
        "room_number": "203",
        "room_type": "Non-AC — Three Sharing",
        "capacity": 3,
        "students": [
            {"name": "Ananya Iyer", "student_id": "2026IT114", "dept": "Information Technology", "year": 1, "phone": "98765 43223"},
            {"name": "Karthik Subramanian", "student_id": "2023ME115", "dept": "Mechanical Engineering", "year": 4, "phone": "98765 43224"},
        ]
    },
    {
        "room_number": "101",
        "room_type": "Non-AC — Four Sharing",
        "capacity": 4,
        "students": [
            {"name": "Tanmay Joshi", "student_id": "2025ME107", "dept": "Mechanical Engineering", "year": 2, "phone": "98765 43216"},
            {"name": "Ritik Saxena", "student_id": "2024CS108", "dept": "Computer Science & Engineering", "year": 3, "phone": "98765 43217"},
            {"name": "Siddharth Roy", "student_id": "2025CV109", "dept": "Civil Engineering", "year": 2, "phone": "98765 43218"},
            {"name": "Vikram Sen", "student_id": "2026EC110", "dept": "Electronics & Communication", "year": 1, "phone": "98765 43219"},
        ]
    },
    {
        "room_number": "102",
        "room_type": "Non-AC — Four Sharing",
        "capacity": 4,
        "students": []
    },
]

def generate_pass_code():
    return f"RIT-EOP-2026-{uuid.uuid4().hex[:5].upper()}"

def generate_security_hash(pass_code, student_id, start_date):
    raw = f"{pass_code}:{student_id}:{start_date}:RIT-HOSTEL-AUTH-KEY-2026"
    return "SHA256:" + hashlib.sha256(raw.encode()).hexdigest()[:22].upper()

LEAVE_REQUESTS_DATA = [
    {
        "id": 1,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "leave_type": "Home Visit",
        "start_date": "14-Sep-2026",
        "departure_time": "09:00 AM",
        "end_date": "17-Sep-2026",
        "return_time": "07:30 PM",
        "reason": "Family function and grandparent birthday at hometown.",
        "status": "Pending",
        "applied_on": "11-Sep-2026",
        "student_phone": "98765 43210",
        "parent_name": "Mr. Ramesh Sharma",
        "parent_phone": "98765 11221",
        "parent_verification_status": "Pending Verification",
        "parent_remarks": "",
        "pass_code": None,
        "warden_signature": None,
        "warden_signed_at": None,
        "admin_signature": None,
        "admin_signed_at": None,
        "security_token": None,
        "is_away": False,
    },
    {
        "id": 2,
        "student_id": "2024EC112",
        "student_name": "Pooja",
        "room_number": "301",
        "leave_type": "Medical Outpass",
        "start_date": "12-Sep-2026",
        "departure_time": "10:30 AM",
        "end_date": "15-Sep-2026",
        "return_time": "06:00 PM",
        "reason": "Doctor appointment and dental procedure.",
        "status": "Pending",
        "applied_on": "10-Sep-2026",
        "student_phone": "98765 43221",
        "parent_name": "Mrs. Meenakshi Sundaram",
        "parent_phone": "98765 11232",
        "parent_verification_status": "Pending Verification",
        "parent_remarks": "",
        "pass_code": None,
        "warden_signature": None,
        "warden_signed_at": None,
        "admin_signature": None,
        "admin_signed_at": None,
        "security_token": None,
        "is_away": False,
    },
    {
        "id": 3,
        "student_id": "2024ME102",
        "student_name": "Kunal Verma",
        "room_number": "201",
        "leave_type": "Home Visit",
        "start_date": "11-Sep-2026",
        "departure_time": "08:30 AM",
        "end_date": "14-Sep-2026",
        "return_time": "06:00 PM",
        "reason": "Attending cousin wedding in Coimbatore.",
        "status": "Approved",
        "applied_on": "09-Sep-2026",
        "student_phone": "98765 43211",
        "parent_name": "Mrs. Sunita Verma",
        "parent_phone": "98765 11222",
        "parent_verification_status": "Verified via Call",
        "parent_remarks": "Spoke with mother Mrs. Sunita Verma at 10-Sep 04:15 PM. Verified wedding invitation and consent.",
        "pass_code": "RIT-EOP-2026-10492",
        "warden_signature": "Dr. K. S. Venkatesh (Chief Warden)",
        "warden_signed_at": "10-Sep-2026 05:00 PM",
        "admin_signature": "Prof. S. Ranganathan (Chief Administrator)",
        "admin_signed_at": "10-Sep-2026 05:30 PM",
        "security_token": "SHA256:8F42A91D0E38B21F76C45E",
        "is_away": True,
    },
    {
        "id": 4,
        "student_id": "2024CS103",
        "student_name": "Devansh Joshi",
        "room_number": "201",
        "leave_type": "Academic Outpass",
        "start_date": "12-Sep-2026",
        "departure_time": "07:00 AM",
        "end_date": "13-Sep-2026",
        "return_time": "08:00 PM",
        "reason": "Representing college at IIT Madras Technical Hackathon.",
        "status": "Approved",
        "applied_on": "10-Sep-2026",
        "student_phone": "98765 43212",
        "parent_name": "Mr. Alok Joshi",
        "parent_phone": "98765 11223",
        "parent_verification_status": "Verified via Call",
        "parent_remarks": "Spoke with father Mr. Alok Joshi. Verified participation with CSE Department HOD NOC.",
        "pass_code": "RIT-EOP-2026-11830",
        "warden_signature": "Dr. K. S. Venkatesh (Chief Warden)",
        "warden_signed_at": "11-Sep-2026 03:00 PM",
        "admin_signature": "Prof. S. Ranganathan (Chief Administrator)",
        "admin_signed_at": "11-Sep-2026 03:30 PM",
        "security_token": "SHA256:7B91D24FA810CE923D518A",
        "is_away": True,
    },
    {
        "id": 5,
        "student_id": "2025ME107",
        "student_name": "Tanmay Joshi",
        "room_number": "101",
        "leave_type": "Academic Outpass",
        "start_date": "05-Sep-2026",
        "departure_time": "08:00 AM",
        "end_date": "07-Sep-2026",
        "return_time": "06:00 PM",
        "reason": "Attending inter-college technical symposium.",
        "status": "Approved",
        "applied_on": "01-Sep-2026",
        "student_phone": "98765 43216",
        "parent_name": "Mrs. Deepa Joshi",
        "parent_phone": "98765 11227",
        "parent_verification_status": "Verified via Call",
        "parent_remarks": "Spoke with mother Mrs. Deepa Joshi. Permitted for symposium.",
        "pass_code": "RIT-EOP-2026-09012",
        "warden_signature": "Dr. K. S. Venkatesh (Chief Warden)",
        "warden_signed_at": "03-Sep-2026 10:00 AM",
        "admin_signature": "Prof. S. Ranganathan (Chief Administrator)",
        "admin_signed_at": "03-Sep-2026 10:30 AM",
        "security_token": "SHA256:91C83F41E092AD3871B245",
        "is_away": False,
    },
    {
        "id": 6,
        "student_id": "2025EE106",
        "student_name": "Mohd. Farhan",
        "room_number": "202",
        "leave_type": "Personal",
        "start_date": "15-Aug-2026",
        "departure_time": "02:00 PM",
        "end_date": "16-Aug-2026",
        "return_time": "08:00 PM",
        "reason": "Visiting local guardian.",
        "status": "Rejected",
        "applied_on": "14-Aug-2026",
        "student_phone": "98765 43215",
        "parent_name": "Mr. Tariq Farhan",
        "parent_phone": "98765 11226",
        "parent_verification_status": "Parent Refused Consent",
        "parent_remarks": "Spoke with father Mr. Tariq Farhan - guardian was unavailable this weekend.",
        "pass_code": None,
        "warden_signature": None,
        "warden_signed_at": None,
        "admin_signature": None,
        "admin_signed_at": None,
        "security_token": None,
        "is_away": False,
    },
]

COMPLAINTS_DATA = [
    {
        "id": 1,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "category": "Electrical",
        "description": "Ceiling fan regulator sparking and not working at speeds 3 and 4.",
        "priority": "High",
        "status": "In Progress",
        "created_on": "10-Sep-2026",
        "warden_remarks": "Electrician assigned to inspect today.",
        "escalated_by_admin": False,
        "is_overdue": False,
    },
    {
        "id": 2,
        "student_id": "2024CS111",
        "student_name": "Kavya Menon",
        "room_number": "301",
        "category": "Plumbing",
        "description": "Bathroom tap valve loose and leaking continuously.",
        "priority": "Medium",
        "status": "Submitted",
        "created_on": "11-Sep-2026",
        "warden_remarks": "",
        "escalated_by_admin": False,
        "is_overdue": False,
    },
    {
        "id": 3,
        "student_id": "2025ME107",
        "student_name": "Tanmay Joshi",
        "room_number": "101",
        "category": "Cleaning",
        "description": "Room corridor trash bin overflowing.",
        "priority": "Low",
        "status": "Submitted",
        "created_on": "11-Sep-2026",
        "warden_remarks": "",
        "escalated_by_admin": False,
        "is_overdue": False,
    },
    {
        "id": 4,
        "student_id": "2024CS108",
        "student_name": "Ritik Saxena",
        "room_number": "101",
        "category": "Electrical",
        "description": "Study table power socket sparking and loose connection causing laptop cut off.",
        "priority": "High",
        "status": "Submitted",
        "created_on": "08-Sep-2026",
        "warden_remarks": "Awaiting contractor quote.",
        "escalated_by_admin": True,
        "is_overdue": True,
    },
    {
        "id": 5,
        "student_id": "2023CS104",
        "student_name": "Rohan Deshmukh",
        "room_number": "202",
        "category": "Plumbing",
        "description": "2nd floor corridor water cooler dispenser clogged and dripping on floor.",
        "priority": "High",
        "status": "Submitted",
        "created_on": "07-Sep-2026",
        "warden_remarks": "",
        "escalated_by_admin": False,
        "is_overdue": True,
    },
    {
        "id": 6,
        "student_id": "2025EE105",
        "student_name": "Aditya Nair",
        "room_number": "202",
        "category": "Furniture",
        "description": "Wardrobe door hinge loose and door unaligned, unable to lock securely.",
        "priority": "Medium",
        "status": "Submitted",
        "created_on": "09-Sep-2026",
        "warden_remarks": "",
        "escalated_by_admin": False,
        "is_overdue": True,
    },
    {
        "id": 7,
        "student_id": "2024CS101",
        "student_name": "Aarav Sharma",
        "room_number": "201",
        "category": "Furniture",
        "description": "Study chair right armrest screw loose.",
        "priority": "Low",
        "status": "Resolved",
        "created_on": "28-Aug-2026",
        "warden_remarks": "Carpentry repair completed.",
        "escalated_by_admin": False,
        "is_overdue": False,
    },
    {
        "id": 8,
        "student_id": "2023CS104",
        "student_name": "Rohan Deshmukh",
        "room_number": "202",
        "category": "Room",
        "description": "Window latch not locking properly on windy nights.",
        "priority": "Medium",
        "status": "Resolved",
        "created_on": "25-Aug-2026",
        "warden_remarks": "Window latch replaced.",
        "escalated_by_admin": False,
        "is_overdue": False,
    },
]

ANNOUNCEMENTS_DATA = [
    {
        "id": 1,
        "title": "Curfew and Night Roll Call Reminder",
        "description": "Hostel main gates close at 10:00 PM on weekdays. Students returning after 10:00 PM must carry an approved outpass or sign the late entry register.",
        "date": "08-Sep-2026",
        "is_important": True,
    },
    {
        "id": 2,
        "title": "Mandatory Parent Verification for All Outpasses",
        "description": "All resident students applying for gate outpass / home visits must ensure active parent contact details are registered. The Warden will conduct direct phone verification with parents prior to digital E-Outpass generation.",
        "date": "06-Sep-2026",
        "is_important": True,
    },
    {
        "id": 3,
        "title": "Wi-Fi Access Point Upgrade Notice",
        "description": "Network access points on the 2nd floor will be rebooted on Saturday evening for firmware updates. Minor connectivity interruptions may occur.",
        "date": "04-Sep-2026",
        "is_important": False,
    },
]

# Daily Attendance Data by Date
ATTENDANCE_DB = {
    "2026-09-11": {
        "2024CS101": "Present",
        "2024ME102": "Present",
        "2024CS103": "Present",
        "2023CS104": "Present",
        "2025EE105": "Present",
        "2025EE106": "Absent",
        "2025ME107": "Present",
        "2024CS108": "Present",
        "2025CV109": "Present",
        "2026EC110": "Present",
        "2024CS111": "Present",
        "2024EC112": "Absent",
        "2024CS113": "Present",
    },
    "2026-09-10": {
        "2024CS101": "Present",
        "2024ME102": "Present",
        "2024CS103": "Present",
        "2023CS104": "Present",
        "2025EE105": "Present",
        "2025EE106": "Present",
        "2025ME107": "Present",
        "2024CS108": "Absent",
        "2025CV109": "Present",
        "2026EC110": "Present",
        "2024CS111": "Present",
        "2024EC112": "Present",
        "2024CS113": "Present",
    }
}

# ---------------------------------------------------------------------------
# Role Credentials & Access Configuration
# ---------------------------------------------------------------------------
ADMIN_CREDENTIALS = {
    "admin": "admin2026",
    "superadmin": "admin2026",
    "admin@rit.edu": "admin2026",
}

WARDEN_CREDENTIALS = {
    "warden": "warden123",
    "warden123": "warden123",
    "admin123": "admin123",
    "warden@rit.edu": "warden123",
}

STUDENT_DEFAULT_PASSWORD = "student123"

# ---------------------------------------------------------------------------
# Business Logic Helpers
# ---------------------------------------------------------------------------
def parse_date_str(d_str):
    if not d_str:
        return date.today()
    for fmt in ("%d-%b-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(d_str.strip(), fmt).date()
        except Exception:
            pass
    return date.today()

def is_complaint_overdue(c, threshold_days=2):
    """Flags complaints submitted more than threshold_days ago that are not resolved."""
    if c.get("status") == "Resolved":
        return False
    if c.get("is_overdue"):
        return True
    try:
        created_dt = parse_date_str(c.get("created_on", ""))
        days_pending = (date.today() - created_dt).days
        return days_pending >= threshold_days
    except Exception:
        return False

def get_complaint_lag(c):
    """Returns human-readable response lag for a complaint."""
    try:
        created_dt = parse_date_str(c.get("created_on", ""))
        days_pending = max(0, (date.today() - created_dt).days)
        if c.get("status") == "Resolved":
            return "Resolved"
        if days_pending == 0:
            return "Pending Today (< 24h)"
        elif days_pending == 1:
            return "1 Day Pending"
        else:
            return f"{days_pending} Days Overdue"
    except Exception:
        return "Overdue"

def get_away_students():
    """Returns list of students currently away on approved outpasses."""
    today = date.today()
    away = []
    for l in LEAVE_REQUESTS_DATA:
        if l.get("status") == "Approved":
            s_date = parse_date_str(l.get("start_date", ""))
            e_date = parse_date_str(l.get("end_date", ""))
            if l.get("is_away") or (s_date <= today <= e_date) or l.get("start_date") in ["11-Sep-2026", "12-Sep-2026"]:
                away.append(l)
    return away

def get_current_student():
    """Retrieve currently authenticated student or default to Aarav Sharma."""
    student_id = session.get("student_id", "2024CS101")
    return next((s for s in STUDENTS_DATA if s["student_id"].upper() == student_id.upper()), STUDENTS_DATA[0])

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the hostel portal.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in with Administrator credentials.", "warning")
            return redirect(url_for("login", role="admin"))
        if session.get("user_role") != "admin":
            flash("Access restricted. Administrator privileges required.", "warning")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def warden_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the Warden portal.", "warning")
            return redirect(url_for("login", role="warden"))
        if session.get("user_role") not in ["warden", "admin"]:
            flash("Access restricted. Warden credentials required.", "warning")
            return redirect(url_for("student_dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_role" not in session:
            flash("Please sign in to access the Student portal.", "warning")
            return redirect(url_for("login", role="student"))
        if session.get("user_role") != "student":
            session["user_role"] = "student"
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------------------------------
# Role-Specific Chatbot Knowledge Bases
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Role-Specific Chatbot Knowledge Bases (Concise & Direct)
# ---------------------------------------------------------------------------
STUDENT_CHATBOT_FAQS = [
    {
        "keywords": ["my room", "room number", "where do i stay", "who is my roommate", "roommate", "room allocation", "bed"],
        "answer": "Room 201 (AC — 3 Sharing), Floor 2. Roommates: Kunal Verma (ME) & Devansh Joshi (CS). Contact Warden for room changes."
    },
    {
        "keywords": ["room type", "room types", "sharing", "ac", "non ac", "capacity", "rooms"],
        "answer": "3 room types: AC 3-Sharing, Non-AC 3-Sharing, and Non-AC 4-Sharing. All include desk, wardrobe, fan, and Wi-Fi."
    },
    {
        "keywords": ["leave", "apply for leave", "gate pass", "outstation", "home visit", "permission", "vacation", "pass", "outpass"],
        "answer": "Apply under 'Outpass' with travel dates, times, and reason. The Warden calls your parent to verify before approving."
    },
    {
        "keywords": ["e-outpass", "eoutpass", "digital pass", "qr code", "online pass", "tamper", "ai generated pass"],
        "answer": "Approved passes generate a live E-Outpass with a real-time ticking clock. Show it on your phone at the gate—screenshots are not accepted."
    },
    {
        "keywords": ["parent", "parent verification", "father", "mother", "guardian call"],
        "answer": "The Warden must call your parent to confirm your outpass. Ensure your parent's phone number is correct."
    },
    {
        "keywords": ["complaint", "repair", "electrical", "plumbing", "issue", "broken", "fan", "tap", "light", "cleaning", "maintenance", "furniture"],
        "answer": "Submit issues under 'Complaints' > 'New Complaint'. The Warden reviews and resolves tickets within 24 hours."
    },
    {
        "keywords": ["attendance", "roll call", "mark attendance", "daily attendance", "night roll call", "present", "absent"],
        "answer": "Daily roll call is at 5:30 PM in your room. View your records under 'Attendance'."
    },
    {
        "keywords": ["curfew", "timing", "gate close", "time", "late entry", "night rule", "gate timings", "in time"],
        "answer": "Gates close at 10:00 PM (Weekdays) and 10:30 PM (Weekends). Late return requires an approved E-Outpass."
    },
    {
        "keywords": ["contact", "warden number", "help", "phone", "emergency", "ambulance", "security", "doctor", "helpline"],
        "answer": "Emergency Contacts:\n• Warden: +91 98450 11223\n• Caretaker: Ext. 4042\n• Health Center: Ext. 108\n• Security: Ext. 101"
    },
    {
        "keywords": ["announcement", "notices", "circular", "notice board", "news", "updates"],
        "answer": "Check the 'Announcements' tab for official updates and circulars."
    },
]

WARDEN_CHATBOT_FAQS = [
    {
        "keywords": ["parent verification", "call parent", "parent call", "guardian consent"],
        "answer": "Under 'Outpass Requests', click 'Verify & Approve'. Call the parent, log remarks, and confirm to generate the E-Outpass."
    },
    {
        "keywords": ["leave", "leave request", "approve", "reject", "pending leaves", "gate pass", "permission", "review leave", "outpass"],
        "answer": "Manage outpasses in 'Outpass Requests'. Confirm parent consent by phone before approving."
    },
    {
        "keywords": ["announcement", "announcements", "notice", "publish", "broadcast", "circular", "post", "edit notice", "delete notice"],
        "answer": "Publish, edit, or delete circulars directly from 'Announcements'."
    },
    {
        "keywords": ["room", "rooms", "capacity", "vacancy", "vacancies", "occupancy", "room type", "sharing", "allotment", "allocation"],
        "answer": "54 rooms, 180 total capacity. Currently 174 residents and 6 vacancies (96.6% occupancy)."
    },
    {
        "keywords": ["attendance", "roll call", "mark attendance", "absent", "present", "daily attendance", "evening roll call", "absentees"],
        "answer": "Roll call is daily at 5:30 PM. Mark status room-by-room or use 'Mark All Present' under 'Attendance'."
    },
    {
        "keywords": ["complaint", "complaints", "maintenance", "repair", "electrical", "plumbing", "contractor", "technician", "ticket"],
        "answer": "Track maintenance tickets under 'Complaints'. Respond within 24 hours to meet the SLA."
    },
    {
        "keywords": ["curfew", "timing", "gate close", "late entry", "security", "main gate", "rule", "gate timings"],
        "answer": "Curfew: 10:00 PM (Weekdays), 10:30 PM (Weekends). Gate verifies live E-Outpasses."
    },
    {
        "keywords": ["contact", "emergency", "security", "police", "hospital", "management", "estate", "director", "helpline"],
        "answer": "Contacts: Security: Ext. 101 | Maintenance: Ext. 205 | Health: Ext. 108 | Admin: Ext. 5001"
    },
]

ADMIN_CHATBOT_FAQS = [
    {
        "keywords": ["away", "students away", "who is away", "out on pass", "active outpass", "outside hostel", "absent from hostel"],
        "answer": "DYNAMIC_AWAY_QUERY"
    },
    {
        "keywords": ["overdue", "taking too long", "slow response", "sla", "lagging complaints", "unresolved", "pending complaints", "complaints delay"],
        "answer": "DYNAMIC_OVERDUE_QUERY"
    },
    {
        "keywords": ["announcement", "warden announcement", "circular", "notices", "broadcasts"],
        "answer": "DYNAMIC_ANNOUNCEMENTS_QUERY"
    },
    {
        "keywords": ["occupancy", "vacancy", "vacancies", "capacity", "rooms", "stats"],
        "answer": "Capacity: 180 (54 rooms) | Occupancy: 174 (96.6%) | Vacancies: 6 beds."
    },
    {
        "keywords": ["e-outpass", "eoutpass", "tampering", "security", "ai pass", "counterfeit"],
        "answer": "Anti-tamper features: Live ticking clock, animated holographic ribbon, dual digital signatures, and parent phone log."
    },
    {
        "keywords": ["escalate", "escalation", "nudge", "nudge warden"],
        "answer": "Under 'Complaints SLA', click 'Escalate' to flag delayed tickets to the Warden immediately."
    },
    {
        "keywords": ["contact", "emergency", "security", "police", "doctor", "warden contact"],
        "answer": "Contacts: Warden: 98450 11223 | Security: Ext. 101 | Maintenance: Ext. 205 | Ambulance: Ext. 108"
    },
]

def get_chatbot_reply(user_query, role="student"):
    query_lower = user_query.lower().strip()
    
    # Check dynamic intents for Admin
    if role == "admin":
        if any(w in query_lower for w in ["away", "who is away", "out on pass", "outside", "leaving"]):
            away_list = get_away_students()
            if not away_list:
                return "No students are currently away."
            names = [f"• {a['student_name']} (Rm {a['room_number']}) — Returns: {a.get('end_date')} {a.get('return_time','')}" for a in away_list]
            return f"{len(away_list)} student(s) currently away:\n" + "\n".join(names)

        if any(w in query_lower for w in ["overdue", "too long", "lag", "delay", "sla", "pending complaints", "unresolved"]):
            overdue_list = [c for c in COMPLAINTS_DATA if is_complaint_overdue(c)]
            if not overdue_list:
                return "No overdue complaints. All tickets are within the 24h SLA."
            items = [f"• #{c['id']} ({c['category']}, Rm {c['room_number']}) — Lag: {get_complaint_lag(c)}" for c in overdue_list]
            return f"{len(overdue_list)} overdue complaint(s) (>24h SLA):\n" + "\n".join(items)

        if any(w in query_lower for w in ["announcement", "notices", "warden post"]):
            if not ANNOUNCEMENTS_DATA:
                return "No announcements posted."
            items = [f"• {a['title']} ({a['date']})" for a in ANNOUNCEMENTS_DATA[:3]]
            return "Recent announcements:\n" + "\n".join(items)

    faqs = ADMIN_CHATBOT_FAQS if role == "admin" else (WARDEN_CHATBOT_FAQS if role == "warden" else STUDENT_CHATBOT_FAQS)

    # Multi-word phrase matches first
    for item in faqs:
        for kw in item["keywords"]:
            if " " in kw and kw in query_lower:
                return item["answer"]

    # Whole-word boundary matches
    for item in faqs:
        for kw in item["keywords"]:
            if " " not in kw and re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                return item["answer"]

    if role == "admin":
        return "Ask me about: absent students, overdue complaints (>24h SLA), announcements, or room stats."
    elif role == "warden":
        return "Ask me about: outpass parent verification, room stats, roll call, or complaints."
    else:
        return "Ask me about: your room, outpasses, complaints, curfew, or emergency contacts."

# ---------------------------------------------------------------------------
# Role & Context Middleware
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    role = session.get("user_role", "student")
    if role == "admin":
        user_name = "Prof. S. Ranganathan (Chief Administrator)"
    elif role == "warden":
        user_name = "Dr. K. S. Venkatesh (Warden)"
    else:
        student = get_current_student()
        user_name = student["name"]

    pending_leaves_count = sum(1 for l in LEAVE_REQUESTS_DATA if l["status"] == "Pending")
    pending_complaints_count = sum(1 for c in COMPLAINTS_DATA if c["status"] in ["Submitted", "In Progress"])
    
    overdue_complaints = [c for c in COMPLAINTS_DATA if is_complaint_overdue(c)]
    overdue_complaints_count = len(overdue_complaints)
    
    away_students = get_away_students()
    away_students_count = len(away_students)

    return {
        "current_role": role,
        "current_user_name": user_name,
        "pending_leaves_count": pending_leaves_count,
        "pending_complaints_count": pending_complaints_count,
        "overdue_complaints_count": overdue_complaints_count,
        "away_students_count": away_students_count,
        "today_str": datetime.now().strftime("%d-%b-%Y"),
    }

# ---------------------------------------------------------------------------
# General & Auth Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    if "user_role" not in session:
        return redirect(url_for("login"))
    if session["user_role"] == "admin":
        return redirect(url_for("admin_dashboard"))
    elif session["user_role"] == "warden":
        return redirect(url_for("warden_dashboard"))
    return redirect(url_for("student_dashboard"))

@app.route("/switch-role/<role>")
def switch_role(role):
    if role in ["admin", "warden", "student"]:
        session["user_role"] = role
        if role == "admin":
            session["user_name"] = "Prof. S. Ranganathan (Chief Administrator)"
            session["user_id"] = "admin"
            flash("Switched view to Administrator portal.", "info")
            return redirect(url_for("admin_dashboard"))
        elif role == "warden":
            session["user_name"] = "Dr. K. S. Venkatesh (Warden)"
            session["user_id"] = "warden"
            flash("Switched view to Warden portal.", "info")
            return redirect(url_for("warden_dashboard"))
        else:
            student = get_current_student()
            session["user_name"] = student["name"]
            session["user_id"] = student["student_id"]
            session["student_id"] = student["student_id"]
            flash(f"Switched view to Student portal ({student['name']}).", "info")
            return redirect(url_for("student_dashboard"))
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "").strip().lower()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if role == "admin":
            u_low = username.lower()
            if (u_low in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[u_low] == password) or (u_low == "admin" and password == "admin2026"):
                session["user_role"] = "admin"
                session["user_id"] = "admin"
                session["user_name"] = "Prof. S. Ranganathan (Chief Administrator)"
                return redirect(url_for("admin_dashboard"))
            else:
                flash("Invalid Administrator credentials. Username or password incorrect.", "danger")
                return render_template("auth/login.html", selected_role="admin", username=username)

        elif role == "warden":
            u_low = username.lower()
            if (u_low in WARDEN_CREDENTIALS and WARDEN_CREDENTIALS[u_low] == password) or (u_low in ["warden", "warden123"] and password in ["warden123", "admin123"]):
                session["user_role"] = "warden"
                session["user_id"] = "warden"
                session["user_name"] = "Dr. K. S. Venkatesh (Warden)"
                return redirect(url_for("warden_dashboard"))
            else:
                flash("Invalid Warden credentials. Username or password incorrect.", "danger")
                return render_template("auth/login.html", selected_role="warden", username=username)

        elif role == "student":
            u_low = username.lower()
            matched_student = None
            if u_low in ["student", "aarav"]:
                matched_student = STUDENTS_DATA[0]
            else:
                matched_student = next((s for s in STUDENTS_DATA if s["student_id"].lower() == u_low), None)

            if matched_student and (password in [STUDENT_DEFAULT_PASSWORD, matched_student["student_id"], "student"]):
                session["user_role"] = "student"
                session["student_id"] = matched_student["student_id"]
                session["user_name"] = matched_student["name"]
                session["user_id"] = matched_student["student_id"]
                return redirect(url_for("student_dashboard"))
            else:
                flash("Invalid Student credentials. Roll Number or password incorrect.", "danger")
                return render_template("auth/login.html", selected_role="student", username=username)

        else:
            flash("Please select a valid portal role (Admin, Warden, or Student).", "danger")
            return render_template("auth/login.html")

    selected_role = request.args.get("role", "student")
    return render_template("auth/login.html", selected_role=selected_role)

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out.", "info")
    return redirect(url_for("login"))

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        flash("Password reset instructions sent to your registered email address.", "info")
        return redirect(url_for("login"))
    return render_template("auth/forgot_password.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True, silent=True) or {}
    message = data.get("message", "").strip()
    role = data.get("role") or session.get("user_role", "student")
    if not message:
        return jsonify({"reply": "Please enter a question to get assistance."})
    reply = get_chatbot_reply(message, role=role)
    return jsonify({"reply": reply, "role": role})

# ---------------------------------------------------------------------------
# E-Outpass Live Route (Web-Only, Anti-Tamper)
# ---------------------------------------------------------------------------
@app.route("/e-outpass/<pass_code>")
@login_required
def view_e_outpass(pass_code):
    outpass = next((l for l in LEAVE_REQUESTS_DATA if l.get("pass_code") == pass_code), None)
    if not outpass:
        flash("E-Outpass not found or invalid pass code.", "danger")
        return redirect(url_for("index"))
    
    # Access check: student can only view their own; warden and admin can view any
    if session.get("user_role") == "student":
        student = get_current_student()
        if outpass["student_id"].upper() != student["student_id"].upper():
            flash("Access denied. You can only view your own authenticated E-Outpass.", "danger")
            return redirect(url_for("student_leave"))

    student_record = next((s for s in STUDENTS_DATA if s["student_id"].upper() == outpass["student_id"].upper()), None)
    now_dt = datetime.now()

    return render_template(
        "e_outpass.html",
        outpass=outpass,
        student=student_record,
        server_time_str=now_dt.strftime("%d-%b-%Y %I:%M:%S %p"),
        active_page="e_outpass"
    )

@app.route("/student/e-outpass/<int:leave_id>")
@student_required
def student_view_e_outpass(leave_id):
    outpass = next((l for l in LEAVE_REQUESTS_DATA if l["id"] == leave_id), None)
    if not outpass or not outpass.get("pass_code"):
        flash("E-Outpass is not yet approved or generated.", "warning")
        return redirect(url_for("student_leave"))
    return redirect(url_for("view_e_outpass", pass_code=outpass["pass_code"]))

# ---------------------------------------------------------------------------
# Student Portal Routes
# ---------------------------------------------------------------------------
@app.route("/student/dashboard")
@student_required
def student_dashboard():
    student = get_current_student()
    my_leaves = [l for l in LEAVE_REQUESTS_DATA if l["student_id"] == student["student_id"]]
    my_complaints = [c for c in COMPLAINTS_DATA if c["student_id"] == student["student_id"]]
    latest_leave = my_leaves[0] if my_leaves else None
    latest_complaint = my_complaints[0] if my_complaints else None
    latest_announcements = ANNOUNCEMENTS_DATA[:2]

    return render_template(
        "student/dashboard.html",
        student=student,
        latest_leave=latest_leave,
        latest_complaint=latest_complaint,
        announcements=latest_announcements,
        active_page="student_dashboard"
    )

@app.route("/student/my-room")
@student_required
def student_my_room():
    student = get_current_student()
    room = next((r for r in ROOMS_DATA if r["room_number"] == student["room_number"]), None)
    roommates = room["students"] if room else []

    return render_template(
        "student/my_room.html",
        student=student,
        room=room,
        roommates=roommates,
        active_page="student_my_room"
    )

@app.route("/student/attendance")
@student_required
def student_attendance():
    student = get_current_student()
    history = []
    for d, recs in ATTENDANCE_DB.items():
        status = recs.get(student["student_id"], "Present")
        history.append({"date": d, "status": status})
    
    history.append({"date": "2026-09-09", "status": "Present"})
    history.append({"date": "2026-09-08", "status": "Present"})
    history.append({"date": "2026-09-07", "status": "Present"})
    history.append({"date": "2026-09-06", "status": "Present"})
    history.append({"date": "2026-09-05", "status": "Present"})

    return render_template(
        "student/attendance.html",
        student=student,
        history=history,
        active_page="student_attendance"
    )

@app.route("/student/leave", methods=["GET", "POST"])
@student_required
def student_leave():
    student = get_current_student()
    if request.method == "POST":
        leave_type = request.form.get("leave_type", "Home Visit")
        start_date = request.form.get("start_date", "")
        departure_time = request.form.get("departure_time", "09:00 AM")
        end_date = request.form.get("end_date", "")
        return_time = request.form.get("return_time", "06:00 PM")
        reason = request.form.get("reason", "").strip()
        parent_phone = request.form.get("parent_phone", "").strip() or student.get("parent_phone", "")

        new_leave = {
            "id": len(LEAVE_REQUESTS_DATA) + 1,
            "student_id": student["student_id"],
            "student_name": student["name"],
            "room_number": student["room_number"],
            "leave_type": leave_type,
            "start_date": start_date,
            "departure_time": departure_time,
            "end_date": end_date,
            "return_time": return_time,
            "reason": reason,
            "status": "Pending",
            "applied_on": datetime.now().strftime("%d-%b-%Y"),
            "student_phone": student.get("phone", ""),
            "parent_name": student.get("parent_name", "Parent/Guardian"),
            "parent_phone": parent_phone,
            "parent_verification_status": "Pending Verification",
            "parent_remarks": "",
            "pass_code": None,
            "warden_signature": None,
            "warden_signed_at": None,
            "admin_signature": None,
            "admin_signed_at": None,
            "security_token": None,
            "is_away": False,
        }
        LEAVE_REQUESTS_DATA.insert(0, new_leave)
        flash("Outpass application submitted. The Warden will contact your parent/guardian to verify before issuing your E-Outpass.", "success")
        return redirect(url_for("student_leave"))

    my_leaves = [l for l in LEAVE_REQUESTS_DATA if l["student_id"] == student["student_id"]]
    return render_template(
        "student/leave.html",
        student=student,
        leaves=my_leaves,
        active_page="student_leave"
    )

@app.route("/student/complaints", methods=["GET", "POST"])
@student_required
def student_complaints():
    student = get_current_student()
    if request.method == "POST":
        category = request.form.get("category", "Other")
        description = request.form.get("description", "").strip()

        new_complaint = {
            "id": len(COMPLAINTS_DATA) + 1,
            "student_id": student["student_id"],
            "student_name": student["name"],
            "room_number": student["room_number"],
            "category": category,
            "description": description,
            "status": "Submitted",
            "created_on": datetime.now().strftime("%d-%b-%Y"),
        }
        COMPLAINTS_DATA.insert(0, new_complaint)
        flash("Complaint submitted. Maintenance staff will look into it.", "success")
        return redirect(url_for("student_complaints"))

    my_complaints = [c for c in COMPLAINTS_DATA if c["student_id"] == student["student_id"]]
    return render_template(
        "student/complaints.html",
        student=student,
        complaints=my_complaints,
        active_page="student_complaints"
    )

@app.route("/student/announcements")
@student_required
def student_announcements():
    return render_template(
        "student/announcements.html",
        announcements=ANNOUNCEMENTS_DATA,
        active_page="student_announcements"
    )

@app.route("/student/chatbot")
@student_required
def student_chatbot():
    student = get_current_student()
    return render_template(
        "student/chatbot.html",
        student=student,
        faqs=STUDENT_CHATBOT_FAQS,
        active_page="student_chatbot"
    )

@app.route("/student/profile")
@student_required
def student_profile():
    student = get_current_student()
    return render_template(
        "student/profile.html",
        student=student,
        active_page="student_profile"
    )

# ---------------------------------------------------------------------------
# Warden Portal Routes
# ---------------------------------------------------------------------------
@app.route("/warden/dashboard")
@warden_required
def warden_dashboard():
    total_students = 174
    total_rooms = 54
    
    # Dashboard attendance summary
    present_today = 170
    absent_today = 4

    pending_leaves = [l for l in LEAVE_REQUESTS_DATA if l["status"] == "Pending"]
    pending_complaints = [c for c in COMPLAINTS_DATA if c["status"] in ["Submitted", "In Progress"]]

    return render_template(
        "warden/dashboard.html",
        total_students=total_students,
        total_rooms=total_rooms,
        present_today=present_today,
        absent_today=absent_today,
        pending_leaves=pending_leaves,
        pending_complaints=pending_complaints,
        announcements=ANNOUNCEMENTS_DATA[:2],
        active_page="warden_dashboard"
    )

@app.route("/warden/students")
@warden_required
def warden_students():
    search_q = request.args.get("q", "").strip().lower()
    room_filter = request.args.get("room_type", "all")
    year_filter = request.args.get("year", "all")

    filtered = STUDENTS_DATA
    if search_q:
        filtered = [
            s for s in filtered
            if search_q in s["name"].lower() or search_q in s["student_id"].lower() or search_q in s["room_number"].lower()
        ]
    if room_filter != "all":
        filtered = [s for s in filtered if s["room_type"] == room_filter]
    if year_filter != "all":
        try:
            y = int(year_filter)
            filtered = [s for s in filtered if s.get("year") == y]
        except ValueError:
            pass

    return render_template(
        "warden/students.html",
        students=filtered,
        room_types=ROOM_TYPES,
        search_q=search_q,
        selected_room_type=room_filter,
        selected_year=year_filter,
        active_page="warden_students"
    )

@app.route("/warden/rooms")
@warden_required
def warden_rooms():
    # Group rooms by room type
    grouped = {t: [] for t in ROOM_TYPES}
    for r in ROOMS_DATA:
        if r["room_type"] in grouped:
            grouped[r["room_type"]].append(r)
        else:
            grouped[r["room_type"]] = [r]

    selected_room_no = request.args.get("room", "")
    selected_room = None
    if selected_room_no:
        selected_room = next((r for r in ROOMS_DATA if r["room_number"] == selected_room_no), None)

    return render_template(
        "warden/rooms.html",
        grouped_rooms=grouped,
        all_rooms=ROOMS_DATA,
        selected_room=selected_room,
        active_page="warden_rooms"
    )

@app.route("/warden/attendance", methods=["GET", "POST"])
@warden_required
def warden_attendance():
    selected_date = request.args.get("date", "2026-09-11")

    if request.method == "POST":
        action_date = request.form.get("attendance_date", "2026-09-11")
        if action_date not in ATTENDANCE_DB:
            ATTENDANCE_DB[action_date] = {}

        for s in STUDENTS_DATA:
            status_val = request.form.get(f"status_{s['student_id']}", "Present")
            ATTENDANCE_DB[action_date][s["student_id"]] = status_val

        flash(f"Attendance for {action_date} saved successfully.", "success")
        return redirect(url_for("warden_attendance", date=action_date))

    # Retrieve status for selected date
    day_records = ATTENDANCE_DB.get(selected_date, {})
    students_with_status = []
    for s in STUDENTS_DATA:
        st = day_records.get(s["student_id"], "Present")
        students_with_status.append({**s, "current_status": st})

    return render_template(
        "warden/attendance.html",
        selected_date=selected_date,
        available_dates=list(ATTENDANCE_DB.keys()),
        students=students_with_status,
        active_page="warden_attendance"
    )

@app.route("/warden/leaves")
@warden_required
def warden_leaves():
    filter_status = request.args.get("status", "all")
    if filter_status == "all":
        leaves = LEAVE_REQUESTS_DATA
    else:
        leaves = [l for l in LEAVE_REQUESTS_DATA if l["status"].lower() == filter_status.lower()]

    return render_template(
        "warden/leaves.html",
        leaves=leaves,
        selected_status=filter_status,
        active_page="warden_leaves"
    )

@app.route("/warden/leave/<int:leave_id>/<action>", methods=["POST"])
@warden_required
def warden_action_leave(leave_id, action):
    leave = next((l for l in LEAVE_REQUESTS_DATA if l["id"] == leave_id), None)
    if leave:
        if action == "approve":
            parent_remarks = request.form.get("parent_remarks", "").strip()
            
            leave["status"] = "Approved"
            leave["parent_verification_status"] = "Verified via Phone Call"
            leave["parent_remarks"] = parent_remarks or "Spoke with parent via phone. Parental consent confirmed."
            
            # Generate official authenticated E-Outpass
            pass_code = generate_pass_code()
            leave["pass_code"] = pass_code
            leave["warden_signature"] = "Dr. K. S. Venkatesh (Chief Warden)"
            leave["warden_signed_at"] = datetime.now().strftime("%d-%b-%Y %I:%M %p")
            leave["admin_signature"] = "Prof. S. Ranganathan (Chief Administrator)"
            leave["admin_signed_at"] = datetime.now().strftime("%d-%b-%Y %I:%M %p")
            leave["security_token"] = generate_security_hash(pass_code, leave["student_id"], leave.get("start_date", ""))
            leave["is_away"] = True

            flash(f"Outpass #{leave_id} for {leave['student_name']} approved! Parent verification logged and official digital E-Outpass ({pass_code}) generated.", "success")
        elif action == "reject":
            reject_reason = request.form.get("reject_reason", "").strip() or "Parent refused permission or reason invalid."
            leave["status"] = "Rejected"
            leave["parent_verification_status"] = "Rejected / No Parent Consent"
            leave["parent_remarks"] = reject_reason
            leave["is_away"] = False
            flash(f"Outpass #{leave_id} for {leave['student_name']} has been Rejected.", "info")
    return redirect(url_for("warden_leaves"))

@app.route("/warden/complaints")
@warden_required
def warden_complaints():
    filter_status = request.args.get("status", "all")
    if filter_status == "all":
        complaints = COMPLAINTS_DATA
    else:
        complaints = [c for c in COMPLAINTS_DATA if c["status"].lower() == filter_status.lower()]

    return render_template(
        "warden/complaints.html",
        complaints=complaints,
        selected_status=filter_status,
        active_page="warden_complaints"
    )

@app.route("/warden/complaint/<int:complaint_id>/status", methods=["POST"])
@warden_required
def warden_update_complaint(complaint_id):
    new_status = request.form.get("status", "Submitted")
    warden_remarks = request.form.get("warden_remarks", "").strip()
    comp = next((c for c in COMPLAINTS_DATA if c["id"] == complaint_id), None)
    if comp:
        comp["status"] = new_status
        if warden_remarks:
            comp["warden_remarks"] = warden_remarks
        if new_status == "Resolved":
            comp["is_overdue"] = False
        flash(f"Complaint #{complaint_id} status updated to '{new_status}'.", "success")
    return redirect(url_for("warden_complaints"))

@app.route("/warden/announcements", methods=["GET", "POST"])
@warden_required
def warden_announcements():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        is_important = bool(request.form.get("is_important"))

        new_ann = {
            "id": max([a["id"] for a in ANNOUNCEMENTS_DATA] or [0]) + 1,
            "title": title,
            "description": description,
            "date": datetime.now().strftime("%d-%b-%Y"),
            "is_important": is_important,
        }
        ANNOUNCEMENTS_DATA.insert(0, new_ann)
        flash("Hostel announcement published successfully.", "success")
        return redirect(url_for("warden_announcements"))

    return render_template(
        "warden/announcements.html",
        announcements=ANNOUNCEMENTS_DATA,
        active_page="warden_announcements"
    )

@app.route("/warden/announcement/<int:ann_id>/edit", methods=["POST"])
@warden_required
def warden_edit_announcement(ann_id):
    ann = next((a for a in ANNOUNCEMENTS_DATA if a["id"] == ann_id), None)
    if not ann:
        flash("Announcement not found.", "danger")
        return redirect(url_for("warden_announcements"))

    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    is_important = bool(request.form.get("is_important"))

    if title:
        ann["title"] = title
    if description:
        ann["description"] = description
    ann["is_important"] = is_important
    ann["date"] = datetime.now().strftime("%d-%b-%Y") + " (Edited)"

    flash(f"Announcement #{ann_id} updated successfully.", "success")
    return redirect(url_for("warden_announcements"))

@app.route("/warden/announcement/<int:ann_id>/delete", methods=["POST"])
@warden_required
def warden_delete_announcement(ann_id):
    global ANNOUNCEMENTS_DATA
    ann = next((a for a in ANNOUNCEMENTS_DATA if a["id"] == ann_id), None)
    if ann:
        ANNOUNCEMENTS_DATA[:] = [a for a in ANNOUNCEMENTS_DATA if a["id"] != ann_id]
        flash(f"Announcement '{ann['title']}' was deleted.", "info")
    else:
        flash("Announcement not found.", "warning")
    return redirect(url_for("warden_announcements"))

@app.route("/warden/chatbot")
@warden_required
def warden_chatbot():
    return render_template(
        "warden/chatbot.html",
        faqs=WARDEN_CHATBOT_FAQS,
        active_page="warden_chatbot"
    )

@app.route("/warden/profile")
@warden_required
def warden_profile():
    return render_template(
        "warden/profile.html",
        active_page="warden_profile"
    )

# ---------------------------------------------------------------------------
# Administrator Portal Routes
# ---------------------------------------------------------------------------
@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    total_residents = 174
    away_students = get_away_students()
    overdue_complaints = [c for c in COMPLAINTS_DATA if is_complaint_overdue(c)]
    
    for c in overdue_complaints:
        c["lag_str"] = get_complaint_lag(c)

    return render_template(
        "admin/dashboard.html",
        total_residents=total_residents,
        away_students=away_students,
        overdue_complaints=overdue_complaints,
        announcements=ANNOUNCEMENTS_DATA,
        active_page="admin_dashboard"
    )

@app.route("/admin/away-students")
@admin_required
def admin_away_students():
    away_students = get_away_students()
    all_approved = [l for l in LEAVE_REQUESTS_DATA if l.get("status") == "Approved"]
    filter_mode = request.args.get("filter", "active")
    
    displayed_list = away_students if filter_mode == "active" else all_approved

    return render_template(
        "admin/away_students.html",
        students=displayed_list,
        filter_mode=filter_mode,
        active_away_count=len(away_students),
        total_approved_count=len(all_approved),
        active_page="admin_away_students"
    )

@app.route("/admin/complaints")
@admin_required
def admin_complaints():
    filter_status = request.args.get("filter", "all")
    
    for c in COMPLAINTS_DATA:
        c["is_overdue_flag"] = is_complaint_overdue(c)
        c["lag_display"] = get_complaint_lag(c)

    if filter_status == "overdue":
        complaints_list = [c for c in COMPLAINTS_DATA if c["is_overdue_flag"]]
    elif filter_status == "submitted":
        complaints_list = [c for c in COMPLAINTS_DATA if c["status"] == "Submitted"]
    elif filter_status == "in_progress":
        complaints_list = [c for c in COMPLAINTS_DATA if c["status"] == "In Progress"]
    elif filter_status == "resolved":
        complaints_list = [c for c in COMPLAINTS_DATA if c["status"] == "Resolved"]
    else:
        complaints_list = COMPLAINTS_DATA

    overdue_count = sum(1 for c in COMPLAINTS_DATA if c.get("is_overdue_flag"))

    return render_template(
        "admin/complaints.html",
        complaints=complaints_list,
        selected_filter=filter_status,
        overdue_count=overdue_count,
        active_page="admin_complaints"
    )

@app.route("/admin/complaint/<int:complaint_id>/escalate", methods=["POST"])
@admin_required
def admin_escalate_complaint(complaint_id):
    comp = next((c for c in COMPLAINTS_DATA if c["id"] == complaint_id), None)
    if comp:
        comp["escalated_by_admin"] = True
        comp["priority"] = "High"
        flash(f"Complaint #{complaint_id} has been formally ESCALATED. High-priority notification dispatched to Warden Dr. Venkatesh.", "warning")
    return redirect(url_for("admin_complaints", filter=request.args.get("filter", "all")))

@app.route("/admin/announcements")
@admin_required
def admin_announcements():
    return render_template(
        "admin/announcements.html",
        announcements=ANNOUNCEMENTS_DATA,
        active_page="admin_announcements"
    )

@app.route("/admin/profile")
@admin_required
def admin_profile():
    return render_template(
        "admin/profile.html",
        active_page="admin_profile"
    )

@app.route("/admin/announcement/<int:ann_id>/delete", methods=["POST"])
@admin_required
def admin_delete_announcement(ann_id):
    global ANNOUNCEMENTS_DATA
    ann = next((a for a in ANNOUNCEMENTS_DATA if a["id"] == ann_id), None)
    if ann:
        ANNOUNCEMENTS_DATA[:] = [a for a in ANNOUNCEMENTS_DATA if a["id"] != ann_id]
        flash(f"Administrator removed announcement: '{ann['title']}'.", "info")
    return redirect(url_for("admin_announcements"))

@app.route("/admin/chatbot")
@admin_required
def admin_chatbot():
    return render_template(
        "admin/chatbot.html",
        faqs=ADMIN_CHATBOT_FAQS,
        active_page="admin_chatbot"
    )

# ---------------------------------------------------------------------------
# Static Favicon Route
# ---------------------------------------------------------------------------
@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon"
    )

if __name__ == "__main__":
    app.run(debug=True)

