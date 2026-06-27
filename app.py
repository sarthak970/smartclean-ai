
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


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>SmartClean AI</title>

    <style>

        *{
            margin:0;
            padding:0;
            box-sizing:border-box;
            font-family:Arial,sans-serif;
        }

        body{
            background:linear-gradient(135deg,#0f172a,#1e293b,#2563eb);
            color:white;
        }

        nav{
            display:flex;
            justify-content:space-between;
            padding:25px 80px;
            background:rgba(0,0,0,0.2);
            backdrop-filter:blur(10px);
        }

        .logo{
            font-size:32px;
            font-weight:bold;
        }

        nav ul{
            display:flex;
            list-style:none;
            gap:30px;
        }

        nav a{
            color:white;
            text-decoration:none;
            font-size:18px;
        }

        .hero{
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:100px;
            min-height:80vh;
        }

        .hero-text{
            width:50%;
        }

        .hero-text h1{
            font-size:70px;
            margin-bottom:20px;
        }

        .hero-text p{
            font-size:24px;
            color:#d1d5db;
            margin-bottom:30px;
        }

        .btn{
            padding:18px 40px;
            background:#3b82f6;
            color:white;
            border:none;
            border-radius:12px;
            text-decoration:none;
            font-size:20px;
            margin-right:15px;
        }

        .btn:hover{
            background:#2563eb;
        }

        .robot{
            font-size:250px;
            animation:float 3s ease-in-out infinite;
        }

        @keyframes float{
            0%{transform:translateY(0px);}
            50%{transform:translateY(-20px);}
            100%{transform:translateY(0px);}
        }

        .stats{
            display:flex;
            justify-content:center;
            gap:30px;
            margin:50px;
        }

        .card{
            background:rgba(255,255,255,0.1);
            padding:40px;
            width:250px;
            border-radius:20px;
            text-align:center;
            backdrop-filter:blur(15px);
        }

        .card h2{
            font-size:40px;
            color:#60a5fa;
        }

        .features{
            padding:80px;
            text-align:center;
        }

        .feature-grid{
            display:grid;
            grid-template-columns:repeat(3,1fr);
            gap:30px;
            margin-top:40px;
        }

        .feature{
            background:rgba(255,255,255,0.08);
            padding:30px;
            border-radius:20px;
        }

        .feature h3{
            font-size:28px;
            margin-bottom:15px;
        }

    </style>
</head>

<body>

<nav>
    <div class="logo">🤖 SmartClean AI</div>

    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Register</a></li>
        <li><a href="/docs">API</a></li>
    </ul>
</nav>

<section class="hero">

    <div class="hero-text">

        <h1>Clean Data.<br>Power AI.</h1>

        <p>
            Upload messy datasets and get
            AI-ready data automatically.
        </p>

        <a href="/upload" class="btn">Upload Dataset</a>

        <a href="/register" class="btn">Get Started</a>

    </div>

    <div class="robot">
        🤖
    </div>

</section>

<div class="stats">

    <div class="card">
        <h2>10K+</h2>
        <p>Datasets Cleaned</p>
    </div>

    <div class="card">
        <h2>99.9%</h2>
        <p>Accuracy</p>
    </div>

    <div class="card">
        <h2>24/7</h2>
        <p>AI Processing</p>
    </div>

</div>

<section class="features">

    <h1 style="font-size:50px;">Features</h1>

    <div class="feature-grid">

        <div class="feature">
            <h3>🧹 Remove Duplicates</h3>
            <p>Automatically remove duplicate rows.</p>
        </div>

        <div class="feature">
            <h3>📉 Missing Values</h3>
            <p>Handle null values intelligently.</p>
        </div>

        <div class="feature">
            <h3>📊 ML Ready</h3>
            <p>Prepare datasets for machine learning.</p>
        </div>

        <div class="feature">
            <h3>⚡ Fast Processing</h3>
            <p>Clean datasets within seconds.</p>
        </div>

        <div class="feature">
            <h3>📁 CSV Support</h3>
            <p>Supports CSV and Excel files.</p>
        </div>

        <div class="feature">
            <h3>☁ Cloud Access</h3>
            <p>Access your cleaned files anywhere.</p>
        </div>

    </div>

</section>

</body>
</html>
"""


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
