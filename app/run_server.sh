#!/bin/bash
python3 -m gunicorn app:run -w 10 -b 0.0.0.0:80

