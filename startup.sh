#!/bin/bash
source /home/shivam/study/spring16/honors/serc/virtualenv_serc/bin/activate
cd /home/shivam/study/spring16/honors/serc/website
gunicorn -b 127.0.0.1:8000 website.wsgi:application &

