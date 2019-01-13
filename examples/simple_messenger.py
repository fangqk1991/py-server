import threading
import time

from fc_messenger import FCMessenger


class DelayThread(threading.Thread):
    def run(self):
        time.sleep(1)
        print('B: Send message..')
        sender = FCMessenger('127.0.0.1', 6488)
        response = sender.send_message('test', 'Nice to meet you.')
        print('B: Received response: {}'.format(response))


if __name__ == "__main__":

    DelayThread().start()

    receiver = FCMessenger('127.0.0.1', 6488)
    msg = receiver.wait_for_message('test', 0, receipt=False)
    print('A: Received message: {}'.format(msg))
    print('A: reply message...')
    receiver.send_receipt('Accepted')
