#!/bin/bash
curl -X POST https://neuhub-bot.onrender.com/send-daily \
  -H "x-cron-secret: neuhubisbig"
echo "Done! Check your WhatsApp."