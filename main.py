import imp
from aiogram.utils import executor
from config import dp


async def on_startup(_):
    print(' \n OSON BOT ISHLAYAPTI  \n OSON BOT IS WORKING  \n KOLAY BOT ÇALIŞAYUR  \n ................... \n _____------_____ \n ...................')          
          
import menu
import fooddetail
import admin
menu.register(dp)
admin.MenuChangeButtons(dp)
fooddetail.register2(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)



    
    
    
    