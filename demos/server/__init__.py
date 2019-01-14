from fc_messenger import FCServer, FCRouter

# redis host and port
HOST = '127.0.0.1'
PORT = 6379
TEST_API = 'some/api'


class TestServer(FCServer):

    api = FCRouter()

    def __init__(self):
        self.init(HOST, PORT, 'SOME-SERVER-NAME')

    @api.route(TEST_API)
    def xxx(self, context, params):
        index = params['index']
        print('[Server] Received message [{}]'.format(index))
        self.answer(context, 'Welcome. [{}]'.format(index))

