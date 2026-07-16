from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime, timedelta
from pathlib import Path

class Alert(BaseModel):
	station: str
	status: str

app = FastAPI(
	title="ACE-FLOW API",
	description="Flash flood monitoring system API",
	version="0.1.0"
)

IMAGE_DIR = Path("app/static/images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory="app/static")

app.mount("/images", StaticFiles(directory=IMAGE_DIR), name="images")

status_table = [
	{
		"station": "Land View 01",
		"status": "Baseline",
		"level": "Baseline",
		"time": "2026-07-13 12:00",
		"image": None
	}
]

@app.post("/api")
async def receive_alert(station: 
	str = Form(...), 
	status: str = Form(...),
	image: UploadFile | None = File(None)
	):

	image_url = None
	if image:
		filename = make_image_filename(station)
		filepath = IMAGE_DIR / filename

		with open(filepath, "wb") as buffer:
			buffer.write(await image.read())

		image_url = f"/images/{filename}"

	status_table.insert(0, {
		"station": station,
		"status": status,
		"time": (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S"),
		"image": image_url
	})

	if len(status_table) > 10:
		status_table.pop()

	return {"success": True}

def make_image_filename(station: str) -> str:
	timestamp = (datetime.utcnow() + timedelta(hours=7)).strftime("%Y-%m-%d %H:%M:%S")
	safe_station = station.replace(" ", "_")
	return f"{timestamp}_{safe_station}.jpg"

@app.get("/")
def dashboard(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={"status_table": status_table}
	)
