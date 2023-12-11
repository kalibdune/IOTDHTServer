from typing import List
from fastapi import FastAPI, File, UploadFile, status, Header, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = []

@app.get("/")
async def getR():
    return {"hello": "hello"}

@app.get("/lastminute", response_class=HTMLResponse)
async def last_minutes(request: Request, minutes: int):
    global data
    last = []
    current = datetime.now()
    for obj in data:
        if current - obj["time"] <= timedelta(minutes=minutes):
            last.append([f"{obj['time'].hour}:{obj['time'].minute}:{obj['time'].second}", obj["temp"], obj["hum"]])    
    return templates.TemplateResponse("item.html", {"request": request, "last": last})

@app.get("/top", response_class=HTMLResponse)
async def top(request: Request, items: int):
    global data
    print(data[len(data)-items:])
    last = []
    for obj in data[len(data)-items:]:
        last.append([f"{obj['time'].hour}:{obj['time'].minute}:{obj['time'].second}", obj["temp"], obj["hum"]])
    return templates.TemplateResponse("item.html", {"request": request, "last": last})

@app.get("/send")
async def send_data(temp: int, hum: int):
    global data
    data.append({"temp": temp, "hum": hum, "time": datetime.now()})
    