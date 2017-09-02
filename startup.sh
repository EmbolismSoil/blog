#!/bin/bash

cd /home/ubuntu/github/blog/ && source venv/bin/activate && python3 manage.py runserver -h 10.135.47.104 -p 5000 
