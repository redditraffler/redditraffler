import json
import falcon


class Collection(object):
    def on_get(self, req, resp):
        body = {
            'raffles': [
                {'id': '1', 'name': 'first raffle'},
                {'id': '2', 'name': 'second raffle'},
                {'id': '3', 'name': 'third raffle'}
            ]
        }

        resp.body = json.dumps(body)


class Item(object):
    def on_get(self, req, resp, submission_id):
        body = {
            'id': submission_id,
            'msg': 'hello world!'
        }
        resp.body = json.dumps(body)
