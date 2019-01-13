import decimal
import json


class __MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)


class FCException(Exception):
    pass


def json_encode(data):
    try:
        return json.dumps(data, cls=__MyJSONEncoder)
    except:
        pass

    return None


def json_decode(content):
    try:
        return json.loads(str(content))
    except:
        pass

    return None
