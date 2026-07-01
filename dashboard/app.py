from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

import json
import os
import subprocess

app = FastAPI()

# =========================
# 📁 BASE DIRECTORY FIX
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# static & templates (ABSOLUTE PATH)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)


# =========================
# 🏠 HOME PAGE
# =========================
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# =========================
# 📊 GET SCAN DATA
# =========================
@app.get("/data")
def get_data():
    report_path = os.path.join(BASE_DIR, "report.json")

    if not os.path.exists(report_path):
        return {"error": "report.json not found"}

    try:
        with open(report_path) as f:
            data = json.load(f)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


# =========================
# 🔥 RUN SCAN (CLI TRIGGER)
# =========================
@app.get("/scan")
def run_scan():
    try:
        subprocess.run(
            ["garuda", "scan", "--json", "dashboard/report.json"],
            check=True
        )
        return {"status": "scan completed"}
    except Exception as e:
        return {"error": str(e)}