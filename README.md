# Neuhub Daily News Bot

Sends a daily WhatsApp message with curated tech + economy news to the Neuhub community.

---

## Stack
- Python + FastAPI (hosted on Render)
- NewsAPI — fetches headlines
- OpenAI GPT-4o — writes the brief
- Twilio — sends via WhatsApp
- cron-job.org — triggers the endpoint daily

---

## Files
- `bot.py` — core logic (fetch, generate, send)
- `main.py` — FastAPI app with `/send-daily` endpoint
- `requirements.txt` — dependencies

---

## Setup

### 1. Add opted-in numbers to bot.py

Open `bot.py` and add each community member's number to `RECIPIENT_NUMBERS`.
Each number must have opted into the Twilio sandbox by texting:
  `join <your-sandbox-word>`
to your Twilio sandbox number first.

Format: `"whatsapp:+447XXXXXXXXX"`

---

### 2. Deploy to Render

1. Push this folder to a GitHub repo
2. Go to render.com → New → Web Service → connect the repo
3. Set these:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `uvicorn main:app --host 0.0.0.0 --port 10000`

4. Add these Environment Variables in Render's dashboard:

| Variable            | Value                                      |
|---------------------|--------------------------------------------|
| TWILIO_ACCOUNT_SID  | ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx         |
| TWILIO_AUTH_TOKEN   | your auth token                            |
| TWILIO_WA_NUMBER    | +14155238886 (your sandbox number)         |
| OPENAI_API_KEY      | sk-...                                     |
| NEWS_API_KEY        | your newsapi.org key                       |
| NEUHUB_WA_LINK      | https://chat.whatsapp.com/YOURLINK         |
| CRON_SECRET         | make up a long random string e.g. neuhub2025xk |

---

### 3. Set up cron-job.org

1. Go to cron-job.org → Create cronjob
2. URL: `https://your-render-url.onrender.com/send-daily`
3. Method: `POST`
4. Add a custom header:
   - Key: `x-cron-secret`
   - Value: whatever you set as `CRON_SECRET`
5. Schedule: daily at your preferred time (e.g. 8:00 AM)

---

### 4. Test it manually

Once deployed, you can test by hitting the endpoint directly:

```bash
curl -X POST https://your-render-url.onrender.com/send-daily \
  -H "x-cron-secret: your-cron-secret"
```

Or run locally first:
```bash
pip install -r requirements.txt
# set env vars in your terminal, then:
python bot.py
```

---

## Moving beyond the sandbox

When you're ready to send to anyone without opt-in:
1. Apply for a WhatsApp Business number through Meta (meta.com/business)
2. Connect it to Twilio
3. Update `TWILIO_WA_NUMBER` in your env vars

That's it — no code changes needed.
