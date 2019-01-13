import threading
import time

from fc_messenger import FCMessenger


# redis host and port
HOST = '127.0.0.1'
PORT = 6379


class SenderThread(threading.Thread):
    def run(self):

        sender = FCMessenger(HOST, PORT)
        response = sender.send_message('test', 'Hello.')
        print('[Client] Received response: {}'.format(response))

        response = sender.send_message('test', 'Nice to meet you.')
        print('[Client] Received response: {}'.format(response))

        response = sender.send_message('test', 'Bye.')
        print('[Client] Received response: {}'.format(response))


if __name__ == "__main__":

    SenderThread().start()

    times = 0
    receiver = FCMessenger(HOST, PORT)
    print('[Receiver] Waiting message...')
    while True:
        msg = receiver.wait_for_message('test', 0, receipt=False)
        times += 1

        print('[Receiver] Received message: {}'.format(msg))
        receiver.send_receipt('Times: {}'.format(times))

        if msg == 'Bye.':
            break
    print('[Receiver] Close')
