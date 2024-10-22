# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import csv
import googleapiclient.discovery
from datetime import datetime

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyCUFZKyBC51U1kwBTlxwN3IX51mCZO4b1E"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="snippet",
        videoId="q8q3OFFfY6c"
    )
    response = request.execute()

    comments = process_comments(response['items'])
    save_to_csv(comments)

def process_comments(response_items):
    comments = []
    for comment in response_items:
        author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
        comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
        publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
        comment_info = {'author': author, 
                'comment': comment_text, 'published_at': publish_time}
        comments.append(comment_info)
    print(f'Finished processing {len(comments)} comments.')
    return comments

def save_to_csv(comments):
    # Generate a filename with current timestamp.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"youtube_comments_{timestamp}.csv"

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['author', 'comment', 'published_at'])
        writer.writeheader()
        for comment in comments:
            writer.writerow(comment)
    
    print(f"Comments have been saved to {filename}")

if __name__ == "__main__":
    main()