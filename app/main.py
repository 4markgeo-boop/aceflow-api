from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(
	title="ACE-FLOW API",
	description="Flash flood monitoring system API",
	version="0.1.0"
)
templates = Jinja2Templates(directory="app/static")

@app.get("/api")
async def root():
	return {
		"message": "ACE-FLOW API is running"
	}

@app.get("/")
def dashboard(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="app/static/index.html",
		context={"status_table": status_table}
	)
