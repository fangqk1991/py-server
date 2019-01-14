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
    __domain = None

    asyncMode = False
    api = None

    def init(self, host, port, domain):
        self.__host = host
        self.__port = port
        self.__domain = domain

    def request(self, req_api, params=None, waiting=True, timeout=10):
        
        if not params:
            params = {}

        if self.asyncMode:
            waiting = False

        p = params.copy()
        p['fc_server_request_api'] = req_api

        messenger = FCMessenger(self.__host, self.__port)
        if not waiting:
            messenger.send_message(self.__domain, json_encode(p), waiting=False)
            return

        response = messenger.send_message(self.__domain, json_encode(p), waiting=True, timeout=timeout)
        response = json_decode(response)

        if 'data' in response:
            return response['data']

        error = response['error']
        raise FCException(error['msg'])

    def listen(self):
        context = FCMessenger(self.__host, self.__port)
        content = context.wait_for_message(self.__domain, timeout=0, receipt=False)
        params = json_decode(content)

        if not isinstance(params, dict) or 'fc_server_request_api' not in params:
            return context, None, None

        req_api = params['fc_server_request_api']
        params.pop('fc_server_request_api')
        return context, req_api, params

    def answer(self, context, data):
        context.send_receipt(json_encode({'data': data}))

    def throw(self, context, msg):
        error = {'msg': msg, 'code': -1}
        context.send_receipt(json_encode({'error': error}))

    def work(self):

        api_map = self.api.apiMap

        while True:

            context, req_api, params = self.listen()

            if not req_api:
                self.throw(context, 'req api missing')
                continue

            if req_api not in api_map:
                self.throw(context, 'req api not in api map')
                continue

            func = api_map[req_api]

            try:
                if self.asyncMode:
                    self.answer(context, 'OK')
                func(self, context, params)
            except Exception as e:
                self.throw(context, str(e))
