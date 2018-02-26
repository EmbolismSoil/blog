#!/bin/bash
IP=`ifconfig | grep "inet addr" | grep -v "127.0.0.1" | sed "s/inet addr:\([0-9.]*\) .*/\1/g"`

LOG_FILE=blog-`date +%Y%m%d`.log
cd /home/ubuntu/github/blog/ && source venv/bin/activate && python3 manage.py runserver -h $IP -p 5000 &> log/$LOG_FILE
