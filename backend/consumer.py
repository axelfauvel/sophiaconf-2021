"""
Suscribe to a given topic and save JSON compliant messages in REDIS
"""
import argparse
import json
import os
from collections import namedtuple
from time import time

import configargparse
import paho.mqtt.client as mqtt
import redis

Redis = namedtuple("Redis", ["host", "port", "db"])
Mqtt = namedtuple(
    "Mqtt", ["host", "port", "keepalive", "user", "password", "topic"]
)
Config = namedtuple("Config", ["redis", "mqtt"])


def parse_args() -> argparse.Namespace:
    """
    retrieve arguments
    """
    parser = configargparse.ArgParser()
    parser.add("--redis-host", env_var="REDIS_HOST", default="127.0.0.1")
    parser.add("--redis-port", env_var="REDIS_PORT", default=6379)
    parser.add("--redis-db", env_var="REDIS_DB", default=1)
    parser.add("--mqtt-host", env_var="MQTT_HOST", default="127.0.0.1")
    parser.add("--mqtt-port", env_var="MQTT_PORT", default=1883)
    parser.add("--mqtt-keepalive", env_var="MQTT_KEEPALIVE", default=60)
    parser.add("--mqtt-user", env_var="MQTT_USER", default="")
    parser.add("--mqtt-password", env_var="MQTT_PASSWORD", default="")
    parser.add("--mqtt-topic", env_var="MQTT_TOPIC", default="")
    return parser.parse_args()


def on_connect(client, userdata, flags, rc) -> None:
    """
    callback triggered after MQTT connnection
    Print result code and suscribe to configured topic

    :param client: mqtt client
    :type client: [type]
    :param userdata: userdata configured in client
    :type userdata: [type]
    :param flags: [description]
    :type flags: [type]
    :param rc: return code of mqtt connection
    :type rc: [type]
    """
    print(f"Connected with result code {str(rc)}")
    client.subscribe(userdata.mqtt.topic)


def on_message(client, userdata, msg) -> None:
    """
    callback triggered when message is received

    Read message, try to decode a JSON from it
    save it in redis if succeeds

    :param client: mqtt client
    :param userdata: userdata configured in client
    :param msg: Message read from topic
    :type msg: [type]
    """
    # example_message received in MQTT
    # {'time': 50600, 'device': 'green', 'value': 27.112}
    try:
        data = json.loads(msg.payload)
    except json.decoder.JSONDecodeError:
        print(f"received incorrect JSON : {msg.payload}")
        print("ignoring...")
        return

    _redis = redis.StrictRedis(
        host=userdata.redis.host,
        port=userdata.redis.port,
        db=userdata.redis.db,
    )
    _redis.lpush(data["device"], json.dumps(data))
    print(f"Correctly received {data}")


def main():
    """
    retrieves argument, create configuration objects then starts the consumer
    """
    args = parse_args()
    redis_config = Redis(args.redis_host, args.redis_port, args.redis_db)
    mqtt_config = Mqtt(
        args.mqtt_host,
        args.mqtt_port,
        args.mqtt_keepalive,
        args.mqtt_user,
        args.mqtt_password,
        args.mqtt_topic,
    )
    config = Config(redis_config, mqtt_config)

    client = mqtt.Client()
    client.user_data_set(config)
    client.username_pw_set(
        mqtt_config.user,
        password=mqtt_config.password,
    )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_config.host, mqtt_config.port, mqtt_config.keepalive)

    client.loop_forever()


if __name__ == "__main__":
    main()
