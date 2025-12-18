from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def read_root() -> HTMLResponse:
    """Return main page with Docker title."""
    return HTMLResponse(content="<h1>Docker</h1>")


@app.get("/healthcheck")
async def healthcheck() -> dict:
    """Health check endpoint returning service status."""
    return {"status": "ok"}