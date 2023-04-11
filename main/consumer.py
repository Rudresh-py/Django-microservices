import json
import pika
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
django.setup()
from user.models import Product


params = pika.ConnectionParameters('localhost')


connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)
    print(properties.content_type)

    if properties.content_type == 'product created':
        product = Product(id=data['id'], title=data['title'],
                          image=data['image'])
        product.save()
        print('Product created successfully!')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        product.delete()
        print('Product Deleted')
    else:
        print('wrong item')

    print("work done")


channel.basic_consume(queue='main', on_message_callback=callback,
                      auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
