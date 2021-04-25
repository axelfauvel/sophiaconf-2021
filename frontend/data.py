import redis

_redis = redis.StrictRedis(
    host="127.0.0.1",
    port=6379,
    db=1,
)

max_index = _redis.llen("green")
data = _redis.lrange("green", 0, max_index)
