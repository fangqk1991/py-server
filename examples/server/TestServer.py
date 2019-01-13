# coding: utf-8
import threading
import time

from messenger import FCServer, FCRouter


TEST_API = 'some/api'
HOST = '127.0.0.1'
PORT = 6488


class DelayThread(threading.Thread):
    def run(self):
        for i in range(5):
            print('B: requesting.. [{}]'.format(i))
            response = TestServer().request(TEST_API, {'index': i})
            print('B: Received response: {}'.format(response))
            time.sleep(1)


class TestServer(FCServer):

    api = FCRouter()

    def __init__(self):
        self.init(HOST, PORT, 'SOME-SERVER-NAME')

    @api.route(TEST_API)
    def xxx(self, context, params):
        index = params['index']
        print('A: Received message [{}]'.format(index))
        self.answer(context, 'Welcome. [{}]'.format(index))


if __name__ == '__main__':
    DelayThread().start()
    TestServer().work()

