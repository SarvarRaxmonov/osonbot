
from aiogram import  types , Dispatcher



from config import bot,dp



async def FunctionNames(message: types.Message):
          
          await bot.send_message(message.from_user.id,text=f'   .')
          
          

    
def register(dp: Dispatcher):
    dp.register_message_handler(FunctionNames, commands=['starts'])
    
    