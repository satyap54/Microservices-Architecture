import asyncio
import aiormq


async def publish(method, event_id):
    connection = await aiormq.connect('amqps://wdwlltwy:mVmwRY959Xx61jK21X_PfoFr8tcgHIBg@cow.rmq2.cloudamqp.com/wdwlltwy')
    channel = await connection.channel()

    body = bytes(str(event_id), 'utf-8')
    await channel.basic_publish(
        body, exchange='', routing_key='admin'
    )
    
    await connection.close()
