import falcon
from api.controllers import raffles

api = application = falcon.API()

api.add_route('/raffles', raffles.Collection())
api.add_route('/raffles/{submission_id}', raffles.Item())
