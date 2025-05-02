#!/bin/bash
source botenv/bin/activate
nohup python3 user_bot.py &
nohup python3 admin_bot.py &