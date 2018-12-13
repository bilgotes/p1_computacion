#!/bin/bash
(crontab -l 2>/dev/null; echo "*/2 * * * * $PWD/recolector.py") | crontab -
virtualenv .venv && source .venv/bin/activate && pip install -r requirements.txt
