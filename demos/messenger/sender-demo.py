from fc_messenger import FCMessenger


# redis host and port
HOST = '127.0.0.1'
PORT = 6379


if __name__ == "__main__":
    sender = FCMessenger(HOST, PORT)
    response = sender.send_message('test', 'Hello.')
    print('[Client] Received response: {}'.format(response))

    response = sender.send_message('test', 'Nice to meet you.')
    print('[Client] Received response: {}'.format(response))

    response = sender.send_message('test', 'Bye.')
    print('[Client] Received response: {}'.format(response))
