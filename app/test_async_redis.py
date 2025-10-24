import asyncio
import redis.asyncio as aioredis

async def main():
    r = aioredis.from_url("redis://localhost:6379/0")
    await r.lpush("testqueue", "hello")              #type: ignore
    result = await r.lrange("testqueue", 0, -1)      #type:ignore
    print("LRANGE result:", result)

asyncio.run(main())
