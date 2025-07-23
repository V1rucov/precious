#!/bin/bash
export BOT_TOKEN="8032192542:AAE-mmWaOBBVtbubkZfLOWICvqmubkaoKxg"
export ADMIN_ID="1496419877"
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app