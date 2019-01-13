# coding: utf-8
import threading
import time

from fc_messenger import FCServer, FCRouter


# redis host and port
HOST = '127.0.0.1'
PORT = 6379
TEST_API = 'some/api'


class ClientThread(threading.Thread):
    def run(self):
        print('[Client] start.\n---')
        for i in range(5):
            print('[Client] requesting.. [{}]'.format(i))
            response = TestServer().request(TEST_API, {'index': i})
            print('[Client] Received response: {}'.format(response))
            time.sleep(1)
        print('---\nClient end.')


class TestServer(FCServer):

    api = FCRouter()

    def __init__(self):
        self.init(HOST, PORT, 'SOME-SERVER-NAME')

    @api.route(TEST_API)
    def xxx(self, context, params):
        index = params['index']
        print('[Server] Received message [{}]'.format(index))
        self.answer(context, 'Welcome. [{}]'.format(index))


if __name__ == '__main__':
    ClientThread().start()
    TestServer().work()

