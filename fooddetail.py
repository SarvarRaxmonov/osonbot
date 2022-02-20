import imp
from aiogram import Dispatcher , types
from config import bot, dp

async def salomlar(message: types.Message):
    await bot.send_video(message.from_user.id, video="link ",caption="<b> Siz bu videoni OSON botdan yuklab oldiyiz </b>",parse_mode='HTML')
    
    
def register2(dp:Dispatcher):
    dp.register_message_handler(salomlar, commands=['help'])    
    
    
    