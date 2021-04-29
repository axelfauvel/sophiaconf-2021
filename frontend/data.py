import redis
import json


def get_device_data(device):
    """
    retrieve data for a given device from redis
    """
    _redis = redis.StrictRedis(
        host="127.0.0.1",
        port=6379,
        db=1,
    )

    max_index = _redis.llen(device)
    data = _redis.lrange(device, 0, max_index)
    return [json.loads(element) for element in data]
