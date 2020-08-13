from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
Filepath = 'DataFile/한글/json/ranked.json'
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

@app.get('/')
async def main(filepath=Filepath):
    return FileResponse(filepath, media_type="Content-Type: application/json; charset='utf-8'")
