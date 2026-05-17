import os
import requests
from openai import OpenAI
from twilio.rest import Client
from datetime import date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─────────────────────────────────────────────
# CONFIG — loaded from .env file
# ─────────────────────────────────────────────
TWILIO_ACCOUNT_SID  = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN   = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WA_NUMBER    = os.environ.get("TWILIO_WA_NUMBER")
OPENAI_API_KEY      = os.environ.get("OPENAI_API_KEY")
NEWS_API_KEY        = os.environ.get("NEWS_API_KEY")
NEUHUB_WA_LINK      = os.environ.get("NEUHUB_WA_LINK", "https://chat.whatsapp.com/JSnLNiaYunWFqJGexffP1f?mode=gi_t")

# Numbers that have opted into the Twilio sandbox
# Add each member's number here in the format: whatsapp:+447XXXXXXXXX
RECIPIENT_NUMBERS = [
    "whatsapp:+2348174745209",   # replace with real opted-in numbers
    "whatsapp:+447398770615",
    "whatsapp:+447350153364"
]

# ─────────────────────────────────────────────
# STEP 1 — Fetch top tech + economy headlines
# ─────────────────────────────────────────────
def fetch_headlines():
    url = "https://newsapi.org/v2/top-headlines"
    articles = []

    for category in ["technology", "business"]:
        resp = requests.get(url, params={
            "apiKey": NEWS_API_KEY,
            "category": category,
            "language": "en",
            "pageSize": 3,
        })
        data = resp.json()
        articles += data.get("articles", [])

    # Build a clean string of headlines + descriptions for the AI
    headlines_text = ""
    for i, a in enumerate(articles[:6], 1):
        title = a.get("title", "")
        desc  = a.get("description", "") or ""
        source = a.get("source", {}).get("name", "")
        headlines_text += f"{i}. [{source}] {title}\n{desc}\n\n"

    return headlines_text

# ─────────────────────────────────────────────
# STEP 2 — Use OpenAI to write the daily brief
# ─────────────────────────────────────────────
def generate_message(headlines_text, wa_link):
    client = OpenAI(api_key=OPENAI_API_KEY)

    today = date.today().strftime("%A, %d %B %Y")

    prompt = f"""
You are the voice of Neuhub — a tech community for young Nigerians and people of African heritage building careers in tech, especially in the UK and Nigeria.

Today is {today}. Here are today's top tech and economy headlines:

{headlines_text}

Write a daily WhatsApp message for the Neuhub community. The tone should be warm, direct, and conversational — like a knowledgeable friend, not a news anchor. 
Write in plain text only, no markdown, no asterisks, no bullet symbols — WhatsApp will handle formatting.

Structure it like this:
1. A short punchy opener for the day (1 sentence)
2. Pick the 2-3 most relevant stories. For each: a one-line headline summary, then 2-3 sentences explaining why it matters, maybe for young people in tech or anyone watching the economy.
3. A discussion question to spark conversation in the group (make it genuinely interesting, not generic), this is optional, you could add anything else you think would be good to end with.
4. A short warm closing line inviting people to share the community link with someone who'd find this useful: {wa_link}

Keep the whole message under 200 words. Do not use emojis excessively — one or two max, used naturally.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.75,
    )

    return response.choices[0].message.content.strip()

# ─────────────────────────────────────────────
# STEP 3 — Send via Twilio WhatsApp
# ─────────────────────────────────────────────
def send_messages(message_body):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for number in RECIPIENT_NUMBERS:
        msg = client.messages.create(
            from_=f"whatsapp:{TWILIO_WA_NUMBER}",
            to=number,
            body=message_body,
        )
        print(f"Sent to {number} — SID: {msg.sid}")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("Fetching headlines...")
    headlines = fetch_headlines()

    print("Generating message...")
    message = generate_message(headlines, NEUHUB_WA_LINK)

    print("\n--- PREVIEW ---")
    print(message)
    print("--- END PREVIEW ---\n")

    print("Sending to recipients...")
    send_messages(message)
    print("Done.")

if __name__ == "__main__":
    main()
