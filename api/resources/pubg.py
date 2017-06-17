from flask_restful import Resource, reqparse

import secret
import requests
import json


class PUBG(Resource):

    def __init__(self, api_key=secret.PUBG_TRACKER_API_KEY, platform='pc'):
        self.api_key = api_key
        self.platform = platform
        self.pubg_url = "https://pubgtracker.com/api/profile/{}/".format(self.platform)
        self.steam_url = "https://pubgtracker.com/api/search?steamId="
        self.headers = {
            'content-type': "application/json",
            'trn-api-key': api_key
        }

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('player', required=False, type=str, location='args')
        parser.add_argument('steam', required=False, type=str, location='args')

        args = parser.parse_args(strict=False)
        player = args.get('player')
        steam = args.get('steam')

        if player:
            try:
                url = self.pubg_url + player
                response = requests.request("GET", url, headers=self.headers)
                return json.loads(response.text)
            except BaseException as error:
                print('Unhandled exception: ' + str(error))
                raise
        if steam:
            try:
                url = self.steam_url + steam
                response = requests.request("GET", url, headers=self.headers)
                print response.text
                return json.loads(response.text)
            except BaseException as error:
                print('Unhandled exception: ' + str(error))
                raise
