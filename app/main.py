from fastapi import FastAPI

app = FastAPI(
	title="ACE-FLOW API",
	description="Flash flood monitoring system API",
	version="0.1.0"
)

@app.get("/")
async def root():
	return {
		"message": "ACE-FLOW API is running"
	}
