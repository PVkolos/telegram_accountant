import asyncio

from create import dp, bot
from handlers import client


async def main():
    dp.include_routers(client.router)

    client.register_client_handlers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

