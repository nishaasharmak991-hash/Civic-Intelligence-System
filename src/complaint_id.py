import sqlite3
import os
from datetime import datetime


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
# Generate Complaint ID
# ----------------------------------------

def generate_complaint_id():

    today = datetime.now().strftime("%Y%m%d")

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM complaints
        WHERE created_at LIKE ?
        """,
        (datetime.now().strftime("%Y-%m-%d") + "%",)
    )

    count = cursor.fetchone()[0] + 1

    conn.close()

    complaint_id = f"CIS-{today}-{count:04d}"

    return complaint_id