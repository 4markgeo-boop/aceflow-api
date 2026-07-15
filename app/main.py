from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime, timedelta

class Alert(BaseModel):
	station: str
	status: str

app = FastAPI(
	title="ACE-FLOW API",
	description="Flash flood monitoring system API",
	version="0.1.0"
)

templates = Jinja2Templates(directory="app/static")

status_table = [
	{
		"station": "Land View 01",
		"status": "Baseline",
		"time": "2026-07-13 12:00"
	}
]

@app.post("/api")
async def receive_alert(alert: Alert):
	status_table.insert(0, {
		"station": alert.station,
		"status": alert.status,
		"time": (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
	})

	if len(status_table) > 10:
		status_table.pop()

	return {"success": True}

@app.get("/")
def dashboard(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={"status_table": status_table}
	)
