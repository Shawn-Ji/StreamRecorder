#!/bin/bash
setsid Xvfb -ac :7 -screen 0 1280x1024x8 -extension RANDR -nolisten inet6
python3 monolithic_main.py
