import json
from models import Event
import asyncio
import aiormq
import aiormq.types


async def callback(message: aiormq.types.DeliveredMessage):
    print("Received in event")
    #print(dir(message.header.properties.content_type))
    properties = message.header.properties

    #print(message.body)
    data = json.loads(message.body)
   
    if(properties.content_type == 'event_created'):
        new_event = Event(id=data['id'], title=data['title'], image=data['image'])
        await new_event.save()
    elif(properties.content_type == 'event_updated'):
        event = await Event.get(id=data['id'])
        event.title = data['title']
        event.image = data['image']
        await event.save()
    elif(properties.content_type == 'event_deleted'):
        event = await Event.get(id=data)
        await event.delete() 

    await message.channel.basic_ack(
        message.delivery.delivery_tag
    )

async def consume():
    connection = await aiormq.connect('amqps://wdwlltwy:mVmwRY959Xx61jK21X_PfoFr8tcgHIBg@cow.rmq2.cloudamqp.com/wdwlltwy')
    channel = await connection.channel()
    print("started consuming")

    # Declaring queue
    declare_ok = await channel.queue_declare('event')
    consume_ok = await channel.basic_consume(
        declare_ok.queue, callback
    )

def consumer_init():
    loop = asyncio.get_event_loop()
    loop.create_task(consume())
    #loop.run_forever()