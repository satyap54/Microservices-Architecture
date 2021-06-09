# amqps://wdwlltwy:mVmwRY959Xx61jK21X_PfoFr8tcgHIBg@cow.rmq2.cloudamqp.com/wdwlltwy
import pika

params = pika.URLParameters('amqps://wdwlltwy:mVmwRY959Xx61jK21X_PfoFr8tcgHIBg@cow.rmq2.cloudamqp.com/wdwlltwy')

connection = pika.BlockingConnection(params)
channel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='admin', body='hello')