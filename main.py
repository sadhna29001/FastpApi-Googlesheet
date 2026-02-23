from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI()

# -----------------------------
# Google Sheets setup
# -----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)
sheet = client.open("FastAPI_Data").sheet1

# -----------------------------

# Data model
# -----------------------------
class Student(BaseModel):
    name: str
    email: str
    marks: int

# -----------------------------
# Home Page (HTML Form)
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Student Form</title>
            <style>
                body { font-family: Arial; background: #f4f4f4; }
                .box {
                    width: 300px;
                    margin: 100px auto;
                    padding: 20px;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 0 10px gray;
                }
                input, button {
                    width: 100%;
                    padding: 8px;
                    margin: 8px 0;
                }
                button {
                    background: green;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="box">
                <h2>Student Entry</h2>
                <form action="/submit" method="post">
                    <input type="text" name="name" placeholder="Name" required />
                    <input type="email" name="email" placeholder="Email" required />
                    <input type="number" name="marks" placeholder="Marks" required />
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
    </html>
    """

# -----------------------------
# Form Submit Handler
# -----------------------------
@app.post("/submit", response_class=HTMLResponse)
async def submit_form(request: Request):
    form = await request.form()

    name = form["name"]
    email = form["email"]
    marks = int(form["marks"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sheet.append_row([timestamp, name, email, marks])

    return f"""
    <html>
        <body style="font-family:Arial; text-align:center; margin-top:100px;">
            <h2>✅ Data Added Successfully!</h2>
            <p>Name: {name}</p>
            <p>Email: {email}</p>
            <p>Marks: {marks}</p>
            <a href="/">Add Another</a>
        </body>
    </html>
    """