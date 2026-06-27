
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import sqlite3
import pandas as pd
import os

app = FastAPI()

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.commit()

@app.get("/")
def home():
    return {"message":"Welcome to SmartClean AI"}

@app.post("/register")
def register(username:str = Form(...), password:str = Form(...)):
    cur.execute("INSERT INTO users(username,password) VALUES (?,?)",(username,password))
    conn.commit()
    return {"status":"registered"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path,"wb") as f:
        f.write(await file.read())

    df = pd.read_csv(path)
    df = df.drop_duplicates()
    df = df.fillna("Missing")

    cleaned = f"uploads/cleaned_{file.filename}"
    df.to_csv(cleaned,index=False)

    return {"cleaned_file": cleaned}
