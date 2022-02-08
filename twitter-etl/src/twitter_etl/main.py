from dataclasses import dataclass
from dynaconf import Dynaconf
import tweepy
from google.cloud import bigquery
import logging

LOGGER = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix="ARCANE",
    environments=True,
)

@dataclass
class TweetMetrics():

    tweet_id : int
    tweet_number : int
    like_count : int
    retweet_count : int
    reply_count : int
    video_view_count : int

def main(request) -> None:
    
    LOGGER.info(f'Received request {request}')

    auth = tweepy.OAuth2UserHandler(
        client_id=settings.CLIENT_ID, 
        client_secret=settings.CLIENT_SECRET,
        redirect_uri=settings.REDIRECT_URI,
        scope=["tweet.read", "users.read"],     
    )

    tweet_client = tweepy.Client(auth)
    big_query_client = bigquery.Client()
    

    for response in tweepy.Paginator(tweet_client.search_recent_tweets,query=settings.TARGET_HASHTAG, tweet_fields='public_metrics', expansions='attachments.media_keys',media_fields='public_metrics.view_count', max_results=settings.BATCH_NUMBER) :
        
        rows_to_insert = []

        medias = {media['media_key']: media for media in response.includes.media}

        for tweet in response.data :

            video_view_count = 0

            if tweet.attachments.media_keys:
                video_view_count = medias.get(tweet.attachments.media_keys[0]).public_metrics.view_count

            rows_to_insert.append(TweetMetrics(
                    tweet_id=tweet.id,
                    tweet_text=tweet.text,
                    like_count=tweet.public_metrics.like_count,
                    retweet_count=tweet.public_metrics.retweet_count,
                    reply_count=tweet.public_metrics.reply_count,
                    video_view_count=video_view_count
                ))

        LOGGER.info(f'Inserting {len(rows_to_insert)} rows in bigquery s "{settings.DESTINATION_TABLE}" table')

        big_query_client.insert_rows_json(settings.DESTINATION_TABLE, rows_to_insert)

    LOGGER.info('Finished tweets data retrival')

