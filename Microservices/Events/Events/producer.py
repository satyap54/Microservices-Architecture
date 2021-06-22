import asyncio
import aiormq


async def publish(method, event_id):
    connection = await aiormq.connect('')
    channel = await connection.channel()

    body = bytes(str(event_id), 'utf-8')
    await channel.basic_publish(
        body, exchange='', routing_key='admin'
    )
    
    await connection.close()
