import json
import pika
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
params = pika.URLParameters(os.environ['AMQPS_KEY'])

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
