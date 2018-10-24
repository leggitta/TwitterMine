import pandas as pd
import requests
import json
import time
from twitter_auth import BEARER_TOKEN


def query(term, max_results=100, endpoint='30day', outfile='query.pkl'):
    
    # initialize header and search parameters
    headers = {'Authorization': 'Bearer %s' % BEARER_TOKEN}
    params = {"query": term, "maxResults": max_results}
    url = 'https://api.twitter.com/1.1/tweets/search/%s/dev.json' % endpoint
    
    # perform first request
    response = requests.post(url, headers=headers, data=json.dumps(params))
    contents = json.loads(response.content)
    tweets = contents['results']

    # process next page of results
    while 'next' in contents:
        time.sleep(2)  # rate limits: 10 requests/second and 30 requests per minute

        # extract next key
        params.update({'next': contents['next']})

        # perform request
        data = json.dumps(params)
        response = requests.post(url, headers=headers, data=data)
        contents = json.loads(response.content)
        tweets += contents['results']

    # convert to data frame and save
    tweets = pd.DataFrame(tweets)
    tweets.to_pickle(outfile)
    return tweets


if __name__ == "__main__":
    tweets = query('#shipwrecksf')
    print(tweets.head())