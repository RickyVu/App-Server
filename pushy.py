import json
import requests
from django.conf import settings
class PushyAPI:

    @staticmethod
    def sendPushNotification(data, to, options={}):

        '''
        # Insert your Pushy Secret API Key here
        apiKey = settings.PUSHY_API_KEY;

        # Default post data to provided options or empty object
        postData = options

        # Set notification payload and recipients
        postData['to'] = to
        postData['data'] = data

        # Set URL to Send Notifications API endpoint
        req = urllib2.Request('https://api.pushy.me/push?api_key=' + apiKey)

        # Set Content-Type header since we're sending JSON
        req.add_header('Content-Type', 'application/json')

        try:
           # Actually send the push
           urllib2.urlopen(req, json.dumps(postData))
        except urllib2.HTTPError as e:
           # Print response errors
           print("Pushy API returned HTTP error " + str(e.code) + ": " + e.read())
        '''


        apiKey = settings.PUSHY_API_KEY
        url = 'https://api.pushy.me/push?api_key=' + apiKey
        # Default post data to provided options or empty object
        postData = options

        # Set notification payload and recipients
        postData['to'] = to
        postData['data'] = data

        headers = {'Content-Type': 'application/json'}

        # Send the request using the 'url' as the target
        response = requests.post(url, data=json.dumps(postData), headers=headers)

        if response.status_code == 200:
            return 'POST request successful'
            #print('POST request successful')
        else:
            return f'POST request failed with status code {response.status_code}'
            #print(f'POST request failed with status code {response.status_code}')