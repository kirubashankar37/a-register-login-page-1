from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# 1. FIX THE CORS ERROR: This allows React (port 3000) to talk to Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what a User looks like
class User(BaseModel):
    username: str
    email: str
    password: str

# 2. THE REGISTER ENDPOINT
@app.post("/register")
def register_user(user: User):
    try:
        # Connect to the MySQL database you created earlier
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kiruba2420304@", # <--- CHANGE THIS
            database="user_system"
        )
        cursor = db.cursor()
        
        # Insert the data into your 'users' table
        sql = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
        val = (user.username, user.email, user.password)
        
        cursor.execute(sql, val)
        db.commit()
        
        return {"status": "success", "message": "User registered in MySQL!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)