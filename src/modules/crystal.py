import sqlite3
from datetime import datetime

DB_PATH = r"D:\Projects\Dashboard\src\dash.db"

def log_session_insight(category, content):
    """
    L5 Routine: Crystallization.
    Saves a new observation or 'Voice Lift' insight back to the DB.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Logs the interaction so the 'Status' report can see progress
        cursor.execute("""
            INSERT INTO observations (timestamp, category, observation)
            VALUES (?, ?, ?)
        """, (datetime.now().isoformat(), category, content))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"L5 Error: Could not crystallize insight. {e}")
        return False

def get_session_stats():
    """Pulls recent activity for the 'Status' command."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM observations")
        count = cursor.fetchone()[0]
        conn.close()
        return f"Total Insights Crystallized: {count}"
    except:
        return "Stats Unavailable."