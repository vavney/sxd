import asyncio
import aioredis

loop = asyncio.get_event_loop()


async def go():
    redis = await aioredis.create_redis_pool(
        'redis://:foobared@127.0.0.1:6379/1', loop=loop)
    await redis.lpush('my-key1', *['value1','value2','3','4'])
    val = await redis.get('my-key')
    print(val)
    redis.close()
    await redis.wait_closed()


loop.run_until_complete(go())
