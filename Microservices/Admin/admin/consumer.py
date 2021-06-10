import pika, os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()

from events.models import Event

params = pika.URLParameters('amqps://wdwlltwy:mVmwRY959Xx61jK21X_PfoFr8tcgHIBg@cow.rmq2.cloudamqp.com/wdwlltwy')

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print("Received in admin")
    id = int(body.decode("utf-8"))
    event = Event.objects.get(id=id)
    event.attendance += 1
    event.save()
    

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)
print('started consuming')
channel.start_consuming()
channel.close()