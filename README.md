# 简介
基于 redis 的应用间通信服务，Python 版。

### 设计说明
* [基于 Redis 的应用间通信](https://fqk.io/app-to-app-communication/)

### 其他版本
* [PHP 版](https://github.com/fangqk1991/php-server)

### 依赖
* [redis](https://redis.io/)

### 安装
```
pip install git+https://github.com/fangqk1991/py-server.git
```

### Messenger 示例
`receiver-demo.py`

```
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
```

`sender-demo.py`

```
from fc_messenger import FCMessenger

# redis host and port
HOST = '127.0.0.1'
PORT = 6379

sender = FCMessenger(HOST, PORT)
response = sender.send_message('test', 'Hello.')
print('[Client] Received response: {}'.format(response))

response = sender.send_message('test', 'Nice to meet you.')
print('[Client] Received response: {}'.format(response))

response = sender.send_message('test', 'Bye.')
print('[Client] Received response: {}'.format(response))
```

![](https://image.fangqk.com/2019-01-14/messenger-demo-python.jpg)