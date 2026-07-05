import sqlite3
import os


# ----------------------------------------
# Database Path
# ----------------------------------------

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "community.db"
)

DB_PATH = os.path.abspath(DB_PATH)


# ----------------------------------------
# Create Database
# ----------------------------------------

def create_database():

    os.makedirs(
        os.path.dirname(DB_PATH),
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        complaint_id TEXT UNIQUE,

        created_at TEXT,

        category TEXT,

        issue_type TEXT,

        location TEXT,

        complaint TEXT,

        language TEXT,

        source TEXT,

        severity TEXT,

        priority_score INTEGER,

        department TEXT,

        status TEXT,

        image_name TEXT,

        assigned_officer TEXT,

        latitude REAL,

        longitude REAL,

        ai_report TEXT
    )
    """)

    conn.commit()

    conn.close()


# ----------------------------------------
# Save Complaint
# ----------------------------------------

def save_complaint(

    complaint_id,

    created_at,

    category,

    issue_type,

    location,

    complaint,

    language,

    source,

    severity,

    priority_score,

    department,

    status,

    image_name,

    assigned_officer,

    latitude,

    longitude,

    ai_report

):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO complaints(

        complaint_id,

        created_at,

        category,

        issue_type,

        location,

        complaint,

        language,

        source,

        severity,

        priority_score,

        department,

        status,

        image_name,

        assigned_officer,

        latitude,

        longitude,

        ai_report

    )

    VALUES(

    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

    )

    """,

    (

        complaint_id,

        created_at,

        category,

        issue_type,

        location,

        complaint,

        language,

        source,

        severity,

        priority_score,

        department,

        status,

        image_name,

        assigned_officer,

        latitude,

        longitude,

        ai_report

    ))

    conn.commit()

    conn.close()


# ----------------------------------------
# Total Complaints
# ----------------------------------------

def get_total_complaints():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        "SELECT COUNT(*) FROM complaints"

    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ----------------------------------------
# Fetch All Complaints
# ----------------------------------------

def get_all_complaints():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM complaints

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ----------------------------------------
# Update Complaint Status
# ----------------------------------------

def update_status(

    complaint_id,

    new_status

):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    UPDATE complaints

    SET status=?

    WHERE complaint_id=?

    """,

    (

        new_status,

        complaint_id

    ))

    conn.commit()

    conn.close()


# ----------------------------------------
# Search Complaint
# ----------------------------------------

def get_complaint(

    complaint_id

):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM complaints

    WHERE complaint_id=?

    """,

    (

        complaint_id,

    ))

    row = cursor.fetchone()

    conn.close()

    return row
# ----------------------------------------
# High Priority Complaints
# ----------------------------------------

def get_high_priority_count():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE priority_score >= 80
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ----------------------------------------
# Pending Complaints
# ----------------------------------------

def get_pending_count():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE status='Pending'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# ----------------------------------------
# Resolved Complaints
# ----------------------------------------

def get_resolved_count():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM complaints
    WHERE status='Resolved'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total