from fc_messenger import FCMessenger

# redis host and port
HOST = '127.0.0.1'
PORT = 6379

receiver = FCMessenger(HOST, PORT)
print('[Receiver] Waiting message...')
while True:
    msg = receiver.wait_for_message('test', 0, receipt=False)
    print('[Receiver] Received message: {}'.format(msg))
    receiver.send_receipt('You said |{}|'.format(msg))
    if msg == 'Bye.':
        break
print('[Receiver] Close')
