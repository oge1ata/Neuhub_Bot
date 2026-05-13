from fastapi import FastAPI, Header, HTTPException, Response
import os
from bot import fetch_headlines, generate_message, send_messages

app = FastAPI()

# A simple secret token so random people can't trigger your bot
CRON_SECRET = os.environ.get("CRON_SECRET", "neuhubisbig")
NEUHUB_WA_LINK = os.environ.get("NEUHUB_WA_LINK", "https://chat.whatsapp.com/JSnLNiaYunWFqJGexffP1f?mode=gi_t")

@app.get("/ping")
def ping():
    return Response(content="ok", media_type="text/plain")

@app.get("/")
def root():
    return Response(content="ok", media_type="text/plain")

@app.post("/send-daily")
def send_daily(x_cron_secret: str = Header(None)):
    if x_cron_secret != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")
    headlines = fetch_headlines()
    message = generate_message(headlines, NEUHUB_WA_LINK)
    send_messages(message)
    return Response(content="ok", media_type="text/plain")

