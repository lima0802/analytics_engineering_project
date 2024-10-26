import os
import csv
from datetime import datetime
import boto3
from googleapiclient.discovery import build

def run_youtube_etl():
    def main():
        # Disable OAuthlib's HTTPS verification when running locally.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        DEVELOPER_KEY = "AIzaSyCYvm8HALHjI1zZLMAV7nEykNMTtJ6KGog"  # Your API key here

        youtube = build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        request = youtube.commentThreads().list(
            part="snippet",
            videoId="q8q3OFFfY6c"
        )
        response = request.execute()

        comments = process_comments(response['items'])
        save_to_s3(comments)

    def process_comments(response_items):
        comments = []
        for comment in response_items:
            author = comment['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment_text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
            publish_time = comment['snippet']['topLevelComment']['snippet']['publishedAt']
            comment_info = {
                'author': author, 
                'comment': comment_text, 
                'published_at': publish_time
            }
            comments.append(comment_info)
        print(f'Finished processing {len(comments)} comments.')
        return comments

    def save_to_s3(comments):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"youtube_comments_{timestamp}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['author', 'comment', 'published_at'])
            writer.writeheader()
            for comment in comments:
                writer.writerow(comment)

        s3 = boto3.client('s3')
        bucket_name = 'li-airflow-youtube-bucket'
        s3.upload_file(filename, bucket_name, 'youtube_comment.csv')
        
        # Clean up local file after upload
        os.remove(filename)
        
        print(f"Comments have been saved to S3 bucket: s3://li-airflow-youtube-bucket/youtube_comment.csv")

    # Execute the main function.
    main()