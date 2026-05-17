import sqlite3

def reset_database():
    conn = sqlite3.connect('dash.db')
    cursor = conn.cursor()

    # Drop old tables
    cursor.execute("DROP TABLE IF EXISTS constraints")
    cursor.execute("DROP TABLE IF EXISTS observations")
    cursor.execute("DROP TABLE IF EXISTS sliders")

    # Table for forbidden terms and style rules
    cursor.execute("""
        CREATE TABLE constraints (
            id INTEGER PRIMARY KEY,
            type TEXT, -- 'forbidden' or 'style'
            phrase TEXT
        )
    """)

    # Table for Dashboard Slider States (The "Missing Link")
    cursor.execute("""
        CREATE TABLE sliders (
            name TEXT PRIMARY KEY,
            value REAL,
            description TEXT
        )
    """)

    # Table for Crystallized Insights (L5)
    cursor.execute("""
        CREATE TABLE observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            observation TEXT
        )
    """)

    # Seed initial slider states
    slider_defaults = [
        ('creativity', 0.7, 'LLM Temperature/Variance'),
        ('rigor', 0.9, 'Gap Check Sensitivity'),
        ('velocity', 0.5, 'Response Length/Speed')
    ]
    cursor.executemany("INSERT INTO sliders VALUES (?, ?, ?)", slider_defaults)

    conn.commit()
    conn.close()
    print("dash.db Reset Complete. Schema initialized for Hybris Orchestration.")

if __name__ == "__main__":
    reset_database()