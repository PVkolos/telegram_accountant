from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from DB.db import DataBase
from GLOBAL import BOT_API


bot = Bot(token=BOT_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
db = DataBase()
