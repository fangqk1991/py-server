from .FCMessenger import FCMessenger
from .utils import json_encode, json_decode, FCException


class FCRouter:

    def __init__(self):
        self.apiMap = {}

    def route(self, rule):
        def decorator(f):
            self.apiMap[rule] = f
            return f
        return decorator


class FCServer:

    __host = None
    __port = None
    __name = None

    asyncMode = False
    api = None

    def init(self, host, port, name):
        self.__host = host
        self.__port = port
        self.__name = name

    def request(self, req_type, params=None, waiting=True, timeout=10):
        
        if not params:
            params = {}

        if self.asyncMode:
            waiting = False

        p = params.copy()
        p['type'] = req_type

        messenger = FCMessenger(self.__host, self.__port)
        if not waiting:
            messenger.send_message(self.__name, json_encode(p), waiting=False)
            return

        response = messenger.send_message(self.__name, json_encode(p), waiting=True, timeout=timeout)
        response = json_decode(response)

        if 'data' in response:
            return response['data']

        error = response['error']
        raise FCException(error['msg'])

    def listen(self):
        context = FCMessenger(self.__host, self.__port)
        content = context.wait_for_message(self.__name, timeout=0, receipt=False)
        params = json_decode(content)

        if not isinstance(params, dict) or 'type' not in params:
            return context, None, None

        req_type = params['type']
        params.pop('type')
        return context, req_type, params

    def answer(self, context, data):
        context.send_receipt(json_encode({'data': data}))

    def throw(self, context, msg):
        error = {'msg': msg, 'code': -1}
        context.send_receipt(json_encode({'error': error}))

    def work(self):

        api_map = self.api.apiMap

        while True:

            context, req_type, params = self.listen()

            if not req_type:
                self.throw(context, 'params error')
                continue

            if req_type not in api_map:
                self.throw(context, 'req type not in api map')
                continue

            func = api_map[req_type]

            try:
                if self.asyncMode:
                    self.answer(context, 'OK')
                func(self, context, params)
            except Exception as e:
                self.throw(context, str(e))
