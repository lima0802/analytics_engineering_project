# Providing example of retrieve data through API call
# https://github.com/youtube/api-samples

# #!/usr/bin/python

import argparse
import os
import re
import googleapiclient.discovery
from googleapiclient.errors import HttpError

API_KEY = "AIzaSyCUFZKyBC51U1kwBTlxwN3IX51mCZO4b1E"

YOUTUBE = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

SECTION_TYPES = ('allPlaylists', 'completedEvents', 'likedPlaylists',
  'likes', 'liveEvents', 'multipleChannels', 'multiplePlaylists',
  'popularUploads', 'recentActivity', 'recentPosts', 'recentUploads',
  'singlePlaylist', 'upcomingEvents',)
SECTION_STYLES = ('horizontalRow', 'verticalList',)

def print_response(response):
    print(response)

def enable_browse_view(youtube):
    channels_list_response = youtube.channels().list(
        part='brandingSettings',
        mine=True
    ).execute()

    channel = channels_list_response['items'][0]
    channel['brandingSettings']['channel']['showBrowseView'] = True

    youtube.channels().update(
        part='brandingSettings',
        body=channel
    ).execute()

def add_channel_section(youtube, args):
    channels = None
    if args.channels:
        channels = re.split('\s*,\s*', args.channels)
    playlists = None
    if args.playlists:
        playlists = re.split('\s*,\s*', args.playlists)

    body = dict(
        snippet=dict(
            type=args.type,
            style=args.style,
            title=args.title,
            position=args.position
        ),
        contentDetails=dict(
            channels=channels,
            playlists=playlists
        )
    )

    youtube.channelSections().insert(
        part='snippet,contentDetails',
        body=body
    ).execute()


## Types and Styles: You'll need to refer to the YouTube API documentation to understand which types and styles are available.

## Title: You can create this yourself when adding a new section.

## Position: You can decide this when adding the section.

## Playlist IDs: Open a playlist and look at the URL. It will contain "list=PL..." - that PL... is the playlist ID.

## Channel IDs: Go to a channel's main page. The URL will contain "channel/UC..." - that UC... is the channel ID.

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--type', choices=SECTION_TYPES, required=True,
        help='The type of the section to be added.')
    parser.add_argument('--style', choices=SECTION_STYLES, required=True,
        help='The style of the section to be added.')
    parser.add_argument('--title',
        help='The title to display for the new section. This is only used '
             'with the multiplePlaylists or multipleChannels section types.')
    parser.add_argument('--position', type=int,
        help='The position of the new section. Use 0 for the top, '
             'or don\'t set a value for the bottom.')
    parser.add_argument('--playlists',
        help='One or more playlist ids, comma-separated (e.g. PL...).')
    parser.add_argument('--channels',
        help='One or more channel ids, comma-separated (e.g. UC...).')

    args = parser.parse_args()

    try:
        # Before channel shelves will appear on your channel's web page, browse.
        # view needs to be enabled. If you know that your channel already has
        # it enabled, or if you want to add a number of sections before enabling it,
        # you can skip the call to enable_browse_view().
        enable_browse_view(YOUTUBE)
        try:
            add_channel_section(YOUTUBE, args)
            print('Added new channel section.')
        except HttpError as e:
            print('An HTTP error {} occurred:\n{}'.format(e.resp.status, e.content))
    except Exception as e:
        print(f'An error occurred: {e}')