import sqlite3

DB_PATH = r"D:\Projects\Dashboard\src\dash.db"

def get_knowledge_context():
    """Fetches constraints and slider states. Returns a structured dictionary."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # 1. Fetch Constraints
        cursor.execute("SELECT type, phrase FROM constraints")
        rules = cursor.fetchall()
        forbidden = [r[1] for r in rules if r[0] == 'forbidden']
        style = [r[1] for r in rules if r[0] == 'style']
        
        # 2. Fetch Sliders
        sliders = {}
        cursor.execute("SELECT name, value FROM sliders")
        for row in cursor.fetchall():
            sliders[row[0]] = row[1]
            
        conn.close()
        
        return {
            "text": f"Forbidden: {forbidden}\nStyle: {style}",
            "sliders": sliders
        }
    except Exception as e:
        return {"text": f"Error: {e}", "sliders": {"creativity": 0.3}}