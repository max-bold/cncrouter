import asyncio

async def hello():
    asyncio.sleep(5)
    print('hello')


asyncio.run(hello())
print('world')