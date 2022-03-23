
from cgitb import text
from collections import UserDict
from gc import callbacks
from aiogram import  types , Dispatcher
from aiogram.types import InlineKeyboardButton as INb , InlineKeyboardMarkup as INm 
import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot,dp

conn = sqlite3.connect('oson.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()


class FSMuser(StatesGroup):
    bulim_nomi = State()
    
async def starting(message: types.Message):
          start = INm(row_width=2)
          start.insert(INb(text="MENU 🍱", callback_data="menu"))
          
          await bot.send_message(message.from_user.id, text="SALOM MENU : " , reply_markup=start)   
async def BulimNames(call: types.CallbackQuery):
          if call.data == "menu":
                global bulimlar
                bulimlar = INm(row_width=2)
                c.execute(f"SELECT mainproductslist FROM asosiymenu")
                for u in c:
                    bulimlar.insert(INb(text=u['mainproductslist'], callback_data=f"BLL{u['mainproductslist']}"))
                await FSMuser.bulim_nomi.set()         
                await call.message.edit_text('SALOM ', reply_markup=bulimlar)
                
          
async def Product_Of_Bulim(call: types.CallbackQuery, state: FSMContext):
          qabul = call.data
          async with state.proxy() as data:
                data['bulim_nomi'] = qabul   
                if qabul[:3] == "BLL":   
                
                   mahsulotlar = INm(row_width=2)
                
                   c.execute(f"SELECT nomi FROM '{qabul[3:]}'")
                   for p in c:
                            mahsulotlar.insert(INm(text=p['nomi'],callback_data="MLR{p['nomi']}"))
                   mahsulotlar.insert(INm(text="orqaga",callback_data="bekor_mahsulot"))         
                   await call.message.edit_text("Qaysi mahsulotni tanlaysiz",reply_markup=mahsulotlar)
            
async def bekor_qilish_user(call: types.CallbackQuery, state:FSMContext):
        
          if call.data == "bekor_mahsulot":
              
            
              await state.finish()
              await call.message.edit_text("SALOM",reply_markup=bulimlar)
         
           
def register(dp: Dispatcher):
        dp.register_callback_query_handler(BulimNames)
       # dp.register_callback_query_handler(bekor_qilish_user, state="*", text=['bekor_mahsulot'])
        dp.register_message_handler(starting, commands=['start'], state=None)
        dp.register_callback_query_handler(Product_Of_Bulim, state=FSMuser.bulim_nomi)

    
     