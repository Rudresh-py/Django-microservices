import json
import os

import django
import pika

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

# params = pika.URLParameters(
#     'amqps://ivzdrafs:ayWp8Y9LV_TUCuHc5c_g7zQXiDJITB0t@kebnekaise.lmq'
#     '.cloudamqp.com/ivzdrafs')

params = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    print(body)
    id = json.loads(body)
    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=id)
        product.likes = product.likes + 1
        product.save()
        print('Product likes increased!')
    elif properties.content_type == 'product ordered':
        product = Product.objects.get(id=id)
        product.ordered = product.ordered + 1
        product.save()
        print('product is ordered')


channel.basic_consume(queue='admin', on_message_callback=callback,
                      auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
