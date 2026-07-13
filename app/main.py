from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(
	title="ACE-FLOW API",
	description="Flash flood monitoring system API",
	version="0.1.0"
)

templates = Jinja2Templates(directory="app/static")

status_table = [
	{
		"station": "Khao Yai 01",
		"status": "Nominal",
		"time": "2026-07-13 12:00"
	}
]

@app.post("/api")
async def root():
#	status_table.append({
#		"station": station,
#		"status": status,
#		"time": time
#	})

	return {"success": True}

@app.get("/")
def dashboard(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html",
		context={"status_table": status_table}
	)
