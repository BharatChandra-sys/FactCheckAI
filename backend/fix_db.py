"""Fix database: add pub_date column to claim_records if missing."""
import sqlite3, os

db_path = "factchecker.db"
if not os.path.exists(db_path):
    db_path = "fake_news.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("PRAGMA table_info(claim_records)")
cols = [row[1] for row in cur.fetchall()]
print("Existing columns:", cols)

if "pub_date" not in cols:
    cur.execute("ALTER TABLE claim_records ADD COLUMN pub_date DATETIME")
    conn.commit()
    print("SUCCESS: Added pub_date column")
else:
    print("OK: pub_date already exists")

conn.close()
