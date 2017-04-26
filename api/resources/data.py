from flask import jsonify
from flask_restful import Resource, reqparse

from mongo import mongo


class Data(Resource):

    def get(selfs):
        data = []
        cursor = mongo.db['data-temp-moist'].find({}, {"_id": 0, "update_time": 0})
        for entry in cursor:
            data.append(entry)

        return jsonify({"status": "ok", "data": data})