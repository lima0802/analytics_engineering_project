import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs

import os
import googleapiclient.discovery

from googleapiclient.discovery import build

# Set the API key
os.environ['YOUTUBE_API_KEY'] = "AIzaSyCUFZKyBC51U1kwBTlxwN3IX51mCZO4b1E"

# Your API key
api_key = os.environ.get('YOUTUBE_API_KEY')

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Now you can use the 'youtube' object to make API calls
# For example:
request = youtube.channels().list(part="snippet,contentDetails,statistics", id="UC_x5XG1OV2P6uZZ5FSM9Ttw")
response = request.execute()

print(response)