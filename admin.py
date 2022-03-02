from ast import Str
from cgitb import text
from codecs import ignore_errors
from collections import UserDict
from email import message
import imp
from itertools import product
from re import A
from tkinter import PhotoImage
from typing import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove,callback_game, inline_keyboard
from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher , types
from config import bot, dp
import MainButtons as nav
ID = '957831856'

###################################################################################################################


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import sqlite3

conn = sqlite3.connect('oson.db')

c = conn.cursor()

class FSMadmin(StatesGroup):
    bulimjoylash = State()
    name = State()
    photo = State()    
    price = State()
    
class itemkeeper(StatesGroup):
      delitemname = State()
      items = State()

class FSMadminmenu(StatesGroup):
    Mainmenuname = State()
    UpdateMenuItem = State() 
    deletmenuitem = State()
    menurename = State()

async def start_change(message: types.Message):
      if f'{message.from_user.id}' == ID:
           await message.answer("O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.uzgartiruvchilar)
           
           
# Bosh menu changes boshlangan bu yerdan ##########################
          
async def Bosh_menu(callbacks: types.CallbackQuery):
      if f'{callbacks.from_user.id}' == ID:
       
         await bot.delete_message(callbacks.from_user.id,  callbacks.message.message_id)
         UsersId = callbacks.from_user.id
         
         if callbacks.data == "Bosh menu":
             await bot.send_message(UsersId, text="O'zgartirmoqchi bulgan bulimizni tanlang ⬇️ ", reply_markup=nav.Menuuzgartirish)
        
         elif callbacks.data == "Menu qushish":
             await FSMadminmenu.Mainmenuname.set()
             await bot.send_message(UsersId,text="✍️ Menu nomini yozing : ", reply_markup=nav.bekor_qilish_menu)
         
         elif callbacks.data == "Menu uchirish":
                 await FSMadminmenu.deletmenuitem.set()
                # await FSMadminmenu.deletmenuitemcheck.set()
                 c.execute("SELECT * FROM asosiymenu")
                 bulimlar = c.fetchall()
                 vv = list(bulimlar)
                                               
                 await bot.send_message(UsersId,text=f"<b>{vv}</b>\
                                        ✍️ Menu nomini yozing : ", reply_markup=nav.bekor_qilish_menu, parse_mode="HTML")
                 await callbacks.answer(text="TANLAGAN BULIM UCHIB KETADI⚠️", show_alert=True)
         
         elif callbacks.data == 'menu uzgartirish':
                 await FSMadminmenu.menurename.set()
                 c.execute("SELECT * FROM asosiymenu")
                 bulimlar = c.fetchall()
                 vv = list(bulimlar)
                
                 await bot.send_message(UsersId,text=f"<b>{vv} \
                      ✍️ Menu nomini yozing : ", reply_markup=nav.bekor_qilish_menu)
                

async def menu_qush(message: types.Message, state: FSMContext):
        if f'{message.from_user.id}' == ID:
            async with state.proxy() as data:
                data['Mainmenuname'] = message.text
            names = data['Mainmenuname']
            c.execute("INSERT INTO asosiymenu VALUES(?)",(names,))
            c.execute(f"CREATE TABLE '{names}'(rasm text, nomi text, narxi text)")
            conn.commit() 
            await message.reply("Raxmat Asosiy <b>Menuga</b> yangi bo'lim qushildi ✅ \n \n Yana o'zgartirmoqchi bulgan bo'limlaringizni tanlang ⬇️", reply_markup=nav.Menuuzgartirish, parse_mode="HTML")
            await state.finish()

async def menu_uchirish(message: types.Message, state:FSMContext):
        if f'{message.from_user.id}' == ID:
        
            
            async with state.proxy() as data:
                   data['deletmenuitem'] = message.text
            
            names = data['deletmenuitem']
            c.execute(f"""DELETE from asosiymenu WHERE mainproductslist LIKE '{names}'""")
            c.execute(f"DROP  TABLE '{names}'")
        
            conn.commit()
            await message.reply(f"{data['deletmenuitem']}<b> ⚠️ OGOHLANTIRISH BUTUN BO'LIM O'CHIB KETDI</b>", parse_mode="HTML", reply_markup=nav.Menuuzgartirish)
            
            await state.finish()           

async def menurenameall(message: types.Message, state: FSMContext):
        if f'{message.from_user.id}' == ID:
            async with state.proxy() as data:
                data['menurename'] = message.text
            renameitem = data['menurename']
            eski = renameitem[0:renameitem.index(' ')]
            yangi = renameitem[renameitem.index(' '):]
            
          #  c.execute(f"ALTER TABLE {eski} RENAME TO {yangi}")
            c.execute(f"""UPDATE asosiymenu SET mainproductslist = ? WHERE mainproductslist = ?""",(yangi,eski))
            
            await message.reply(f"BO'LIM : <b>{renameitem[0:renameitem.index(' ')]}</b> O'ZGARTIRILDI : <b>{renameitem[renameitem.index(' '):]}</b> ✅", parse_mode="HTML", \
              reply_markup=nav.Menuuzgartirish)
            conn.commit()
            await state.finish()
            
# . small menu  settings boshlanadi bu yerdan ####################
                 
                 
async def small_menu(call: types.CallbackQuery):
        if f'{call.from_user.id}' == ID: 
            global mainprokeyboard
            await bot.delete_message(call.from_user.id,  call.message.message_id)
            UserId = call.from_user.id  
            if call.data == 'Mahsulotni uzgartirish':
                await bot.send_message(UserId, text="O'zgartirmoqchi bulgan bulimizni tanlang ⬇️",reply_markup=nav.Smallmenuuzgartirish, parse_mode="HTML")            
            if call.data == 'smallmenu qushish':
                await FSMadmin.bulimjoylash.set()
                
                c.execute("SELECT * FROM asosiymenu")
                d = list(c.fetchall())
                await bot.send_message(UserId, text=f'{d} \n ✍️ Qaysi bulimga qushamiz | Bulim nomini yozing :', reply_markup=nav.bekor_qilish_menu) 
            if call.data == 'smallmenu uchirish':
                await itemkeeper.delitemname.set()
                
                mainprokeyboard = InlineKeyboardMarkup(row_width=2)
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT mainproductslist FROM asosiymenu")
                for i in c:
            
                        mainprokeyboard.insert(
                        
                            InlineKeyboardButton(text=i['mainproductslist'], callback_data=i['mainproductslist'])
                        
                    )
                await bot.send_message(UserId, text="Qaysi bo'limdagi mahsulotni uchirmoqchisiz : " , reply_markup=mainprokeyboard)
                
                
                
async def bulim_joylash(message: types.Message, state: FSMContext):
       if f'{message.from_user.id}' == ID:
          async with state.proxy() as data:
                data['bulimjoylash'] = message.text
          global bulimj
          bulimj = data['bulimjoylash']  
          await FSMadmin.next()        
          await message.reply("nomini yozing :")    

    
async def load_name(message: types.Message, state: FSMContext):
      if f'{message.from_user.id}' == ID:
         async with state.proxy() as data:
            data['name'] =  message.text
         global loadn
         loadn = data['name']
         bulim = bulimj
         c.execute(f"INSERT INTO '{bulim}' VALUES(?,?,?)",(None,loadn,None))
         conn.commit()
         await FSMadmin.next()
         await message.reply("photoni yuklang")     

async def load_phot(message: types.Message, state: FSMContext):
      if f'{message.from_user.id}' == ID:
        async with state.proxy() as data:
            data['photo'] = message.text
        photoink = data['photo']
        loadname = loadn
        bulim = bulimj
        c.execute(f"UPDATE '{bulim}' SET rasm ='{photoink}' WHERE nomi = '{loadname}'")
        conn.commit()
        await FSMadmin.next()
        await message.reply("price yozing")
 
        # names = data['name']
        # c.execute("INSERT INTO asosiymenu VALUES(?)",(names,))
        # conn.commit()         


#@dp.message_handler(state=FSMadmin)
async def load_price(message: types.Message, state: FSMContext):
      if f'{message.from_user.id}' == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        
            loadprice = data['price']
            loadname = loadn
            bulim = bulimj
            c.execute(f'UPDATE "{bulim}" SET narxi = "{loadprice}" WHERE nomi = "{loadname}"')
            conn.commit()
            await message.reply(f"<b>🖼 Rasm : </b>{data['photo']} \n \n <b>✍️ Nomi : </b>{data['name']} \n \n <b>💰 Narxi : </b>{data['price']} \n \n <b>Malumotlar qushildi ✅</b>", parse_mode="HTML", reply_markup=nav.Smallmenuuzgartirish) 
            
        await state.finish()
    
################################################################### mahsulot uchirish

async def delete_mahsulot(call: types.CallbackQuery, state: FSMContext):
      if f'{call.from_user.id}' == ID:
          global bulimname
          async with state.proxy() as data:
              data['delitemname'] = call.data
              bulimname = data['delitemname']
              UsersId = call.from_user.id
              global products
              products = InlineKeyboardMarkup(row_width=2)
              conn.row_factory = sqlite3.Row
              c = conn.cursor()
              c.execute(f"SELECT nomi FROM '{bulimname}'")
              for i in c:
            
                        products.insert(
                        
                            InlineKeyboardButton(text=i['nomi'], callback_data=i['nomi'])
                            
                        
                    )
              products.insert(InlineKeyboardButton(text='❌ Bekor qilish',callback_data='Bekor qilish small'))
              
              await bot.send_message(UsersId, text=f"Bo'lim nomi : <b>{bulimname}</b> \n uchirmoqchi bulgan <b>mahsulotni</b> tanglang ✅ :" , reply_markup=products, parse_mode="HTML")
              await bot.delete_message(call.from_user.id,  call.message.message_id)
              
              await itemkeeper.next()
            
              
async def pick_delete_item(call: types.CallbackQuery, state: FSMContext):
     if f'{call.from_user.id}' == ID:
         
         async with state.proxy() as data:
             data['items'] = call.data
             delet_item = data['items']
             UserId = call.from_user.id
             c.execute(f"SELECT nomi FROM '{bulimname}'")
             conn.row_factory == sqlite3.Row
             print(bulimname)
             bulimnomi = c.fetchall()
             print(bulimnomi)
             print('bu call data:',call.data)
             if call.data:
                 deleted_items = []
                 deleted_items.append(call.data)
                 
                 delitem =InlineKeyboardButton(text=f"✅ O'chirildi : {call.data}", callback_data=f"o'chirildi")
                 products.add(delitem)
               
                 if call.data != "o'chirildi":
                      await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=products)
                 
                        
             state.finish()
                 
                     
             
         
async def bekor_qilish(callbacks: types.CallbackQuery, state: FSMContext):
      if f'{callbacks.from_user.id}' == ID:
           if callbacks.data == "bekor qilish menu":
              await state.finish()
              await bot.delete_message(callbacks.from_user.id,  callbacks.message.message_id)
              await bot.send_message(callbacks.from_user.id,"O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.uzgartiruvchilar)
           if callbacks.data == 'Bekor qilish small':
              await state.finish()
              await bot.delete_message(callbacks.from_user.id,  callbacks.message.message_id)
              await bot.send_message(callbacks.from_user.id,"O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=mainprokeyboard)


     
#@dp.message_handler(state="*", commands="otmena")
#@dp.message_handler(Text(equals='delete', ignore_case=True),state="*")

# async def cancel_handler(message: types.Message, state: FSMContext):
#             if f'message.from_user.id' == ID:
#                 current_state = await state.get_state()
#                 if current_state is None:
#                     return
#                 await state.finish()
#                 await message.reply('OK')
                
        
    
    
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
                            
def MenuChangeButtons(dp:Dispatcher):
    # dp.register_message_handler(adminwait, commands=['admin'])
    # dp.register_callback_query_handler(boshmenu,text=['Bosh menu','Qushish'])
    
    dp.register_message_handler(start_change,commands=['settings'])
   
    dp.register_message_handler(load_phot, state=FSMadmin.photo)
    dp.register_message_handler(load_name, state=FSMadmin.name) 
    dp.register_message_handler(load_price, state= FSMadmin.price)   
    # dp.register_message_handler(cancel_handler, state="*", commands=['delete'])
    dp.register_callback_query_handler(Bosh_menu, text=['Bosh menu','Menu qushish','Menu uchirish','menu uzgartirish'], state=None)
    dp.register_callback_query_handler(small_menu, text=['Mahsulotni uzgartirish','smallmenu qushish', 'smallmenu uchirish','smallmenu uzgartirish'], state=None)
    dp.register_message_handler(menu_qush,state= FSMadminmenu.Mainmenuname)
    dp.register_message_handler(menu_uchirish,state= FSMadminmenu.deletmenuitem)
    
    dp.register_message_handler(menurenameall, state=FSMadminmenu.menurename)
    dp.register_callback_query_handler(bekor_qilish, state="*",text=['bekor qilish menu', 'Bekor qilish small'])
    dp.register_message_handler(bulim_joylash, state=FSMadmin.bulimjoylash)
    dp.register_callback_query_handler(delete_mahsulot, state=itemkeeper.delitemname)
    dp.register_callback_query_handler(pick_delete_item, state=itemkeeper.items)
# for c in range(1,115):
      
  
#     if c < 31:
        
              
#                sura1.insert(InlineKeyboardButton(text=c, callback_data=f"sura3{c}"));    
    
    
    
    