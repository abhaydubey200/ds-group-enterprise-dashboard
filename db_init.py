import bcrypt
from database import get_connection

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(255),
        role VARCHAR(20)
    )
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS upload_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        file_name VARCHAR(255),
        table_name VARCHAR(255),
        rows_uploaded INT,
        duplicates_removed INT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        hashed = bcrypt.hashpw("Admin@123".encode(), bcrypt.gensalt()).decode()
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (%s,%s,%s)",
            ("admin", hashed, "admin")
        )
        print("Default admin created: username=admin, password=Admin@123")
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
