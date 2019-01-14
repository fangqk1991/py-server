import time
from demos.server import TestServer, TEST_API

client = TestServer()
print('[Client] start.\n---')
for i in range(5):
    print('[Client] requesting.. [{}]'.format(i))
    response = client.request(TEST_API, {'index': i})
    print('[Client] Received response: {}'.format(response))
    time.sleep(1)
print('---\nClient end.')
