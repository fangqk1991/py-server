# coding: utf-8
import redis
import uuid


class FCMessenger:

    __redisDB = None
    __sessionID = None

    def __init__(self, host, port):
        self.__redisDB = redis.StrictRedis(host=host, port=port, db=0, charset="utf-8", decode_responses=True)

    def __send_api(self, api):
        return 'fc:messenger:api:%s' % api

    def __generate_session_id(self):
        return 'fc:messenger:session:id:%s' % uuid.uuid1()

    def __inner_wait_for_message(self, api, timeout=10):
        item = self.__redisDB.blpop([api], timeout=timeout)
        if item:
            return item[1]
        return None

    def wait_for_message(self, api, timeout=10, receipt=True):
        uid = self.__inner_wait_for_message(self.__send_api(api), timeout)
        content = self.__redisDB.get(uid)

        self.__sessionID = uid

        if receipt:
            self.send_receipt('OK')

        return content

    def send_receipt(self, content):
        if self.__sessionID:
            self.__redisDB.rpush(self.__send_api(self.__sessionID), content)
            self.__sessionID = None

    def send_message(self, api, content, waiting=True, timeout=10):
        session_id = self.__generate_session_id()
        self.__redisDB.set(session_id, content)
        self.__redisDB.expire(session_id, 60)
        self.__redisDB.rpush(self.__send_api(api), session_id)
        if not waiting:
            return
        return self.__inner_wait_for_message(self.__send_api(session_id), timeout=timeout)

