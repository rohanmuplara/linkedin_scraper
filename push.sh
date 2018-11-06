#!/bin/bash
read -p "Enter the commit message: " commit_message
yapf -i linkedin_scraper.py
git add .
git commit -m  "$commit_message"
git push
