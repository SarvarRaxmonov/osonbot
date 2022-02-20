import imp
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()



bot = Bot(token='5286275314:AAGauG71MIjjUPo4huFBpEHdX9c3Ys9wbHs')
dp = Dispatcher(bot, storage=storage)   
