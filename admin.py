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

class Renamemenuall(StatesGroup):
    oldmenurename = State()
    newnamemenu = State()
    
class Renamesmallmenuall(StatesGroup):
    oldsmallitem = State()
    newsmallitem = State()
    item_type_keeper = State()
    text_or_file = State()
async def start_change(message: types.Message):
      if f'{message.from_user.id}' == ID:
           await message.answer("O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.uzgartiruvchilar)
           
           
# Bosh menu changes boshlangan bu yerdan ##########################
          
async def Bosh_menu(callbacks: types.CallbackQuery):
      if f'{callbacks.from_user.id}' == ID:
         global table_names 
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
         
         
         mainprokeyboards = InlineKeyboardMarkup(row_width=2) 
         conn.row_factory = sqlite3.Row
         d = conn.cursor()
         d.execute("SELECT mainproductslist FROM asosiymenu")
                
         for i in d:
                        
                        mainprokeyboards.insert(
                        
                            InlineKeyboardButton(text=i['mainproductslist'], callback_data=i['mainproductslist']),
                        
                    )
         mainprokeyboards.add(InlineKeyboardButton(text="🔙 Orqaga qaytish",callback_data="bekor qilish menu")) 
         
         if callbacks.data == 'menu uzgartirish':
                 await Renamemenuall.oldmenurename.set()
                 await bot.send_message(UsersId,text="O'zgartirmoqchi bulgan bo'limni tanlang : ", reply_markup=mainprokeyboards)
                 

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
            
            state.finish()           

async def oldname_menu(call: types.CallbackQuery, state: FSMContext):
        if f'{call.from_user.id}' == ID:
            if call.data == "bekor qilish menu":
                await state.finish()
                await bot.delete_message(call.from_user.id,  call.message.message_id)
                await bot.send_message(call.from_user.id,"O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.uzgartiruvchilar)
     
            else:    
                global oldname
                UsersId = call.from_user.id
                async with state.proxy() as data:
                    data['menurename'] = call.data
                    oldname = data['menurename']

                    await bot.send_message(UsersId,f"O'zgartirish uchun tanlangan bo'lim : {oldname} \n Yangi nomini yozing 📝:" , reply_markup=nav.bekor_qilish_menu)
                await Renamemenuall.next()
async def uzgartirish_menu_name(message: types.Message, state: FSMContext):
        if f'{message.from_user.id}' == ID:
           
            UserId = message.from_user.id  
            async with state.proxy() as data:
                
                data['newnamemen'] = message.text
                
                newnameitem = data['newnamemen']               
                c.execute(f"""UPDATE asosiymenu SET mainproductslist = ? WHERE mainproductslist = ?""",(newnameitem,oldname))
                c.execute(f"""ALTER TABLE '{oldname}' RENAME TO '{newnameitem}'""")
                await bot.send_message(UserId,f"O'zgartirildi bo'lim : {oldname} \n Yangi nomi : {newnameitem}",\
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
   
   ############################################################
    
            mainprokeyboard = InlineKeyboardMarkup(row_width=2)
            conn.row_factory = sqlite3.Row
            d = conn.cursor()
            d.execute("SELECT mainproductslist FROM asosiymenu")
                
            for i in d:
                        
                        mainprokeyboard.insert(
                        
                            InlineKeyboardButton(text=i['mainproductslist'], callback_data=i['mainproductslist']),
                        
                    )
            mainprokeyboard.add(InlineKeyboardButton(text="🔙 Orqaga qaytish",callback_data="bekor qilish menu"))
            if call.data == 'smallmenu uchirish':
                await itemkeeper.delitemname.set()
                await bot.send_message(UserId, text="Qaysi bo'limdagi mahsulotni uchirmoqchisiz : " , reply_markup=mainprokeyboard)
           
            if call.data == 'smallmenu qushish':
                    await FSMadmin.bulimjoylash.set()
                    await bot.send_message(UserId, text=f'✍️ Qaysi bulimga qushamiz | Bulim nomini bosing', reply_markup=mainprokeyboard) 
                    
            if call.data == "smallmenu uzgartirish": 
                    await Renamesmallmenuall.oldsmallitem.set()                                                                                                                                     
                    await bot.send_message(UserId, text="♻️ Smallmenu o'zgartirsh \n \n Qaysi bo'limda siz izlayotgan mahsulot: " , reply_markup=mainprokeyboard)
                
async def bulim_joylash(call: types.Message, state: FSMContext):
       if f'{call.from_user.id}' == ID:
          async with state.proxy() as data:
                data['bulimjoylash'] = call.data
          global bulimj
          UserId = call.from_user.id  
          bulimj = data['bulimjoylash']  
          await FSMadmin.next()        
          await bot.send_message(UserId,text="Nomini yozing :")    

    
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
              products = InlineKeyboardMarkup(row_width=2,one_time_keyboard=True)
              conn.row_factory = sqlite3.Row
              c = conn.cursor()
              c.execute(f"SELECT nomi FROM '{bulimname}'")
              for i in c:
            
                        products.insert(
                        
                            InlineKeyboardButton(text=i['nomi'], callback_data=i['nomi'])
                            
                        
                    )
              
              products.insert(InlineKeyboardButton(text='⬅️ Orqaga',callback_data='Bekor qilish small'))
              
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
                 
                
                 
                 delitem =InlineKeyboardButton(text=f"✅ O'chirildi : {call.data}", callback_data=f"o'chirildi")
                 products.add(delitem)
                 item_id = c.execute(f"""SELECT rowid FROM '{bulimname}' WHERE nomi = '{call.data}'""")
                
                 uz = item_id.fetchone()
            
                 c.execute(f"""DELETE FROM '{bulimname}' WHERE rowid = ?""",(uz[0],))
               
                 if call.data != "o'chirildi" :
                    
                        
                        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=products)
                 conn.commit()
                    

async def rename_small_menu(call: types.CallbackQuery, state : FSMContext):
    
      if f'{call.from_user.id}' == ID:
          UserId = call.from_user.id
          global oldsmallitem_keep
          global smallrenameMPB
          async with state.proxy() as data:
                  data['oldsmallitem'] = call.data 
                  oldsmallitem_keep = data['oldsmallitem']                 
                  smallrenameMPB = InlineKeyboardMarkup(row_width=2)
                  conn.row_factory = sqlite3.Row
                  d = conn.cursor()
                  d.execute(f"SELECT nomi FROM {oldsmallitem_keep}")
                
                  for i in d:
                        
                        smallrenameMPB.insert(
                        
                            InlineKeyboardButton(text=i['nomi'], callback_data=i['nomi']),
                        
                    )
                  mainprokeyboard.add(InlineKeyboardButton(text="🔙 Orqaga qaytish",callback_data="bekor qilish menu"))
                  await bot.send_message(UserId, text="♻️ Smallmenu o'zgartirsh \n \n Qaysi <b>mahsulotni</b> o'zgartirasiz :" , reply_markup=smallrenameMPB, parse_mode="HTML")
          await Renamesmallmenuall.next()                
async def newname_small_type_giver(call: types.CallbackQuery, state: FSMContext):
      if f"{call.from_user.id}" == ID:
          UserId = call.from_user.id
          async with state.proxy() as data:
                data['newsmallitem'] = call.data
                newsmall = data['newsmallitem']
                
                newsmallmarkup = InlineKeyboardMarkup(row_width=2)
                newsmallmarkup.add(InlineKeyboardButton(text="🌉 Rasm",callback_data="rasm"),InlineKeyboardButton(text="📋 Nomi",callback_data="nomi"),InlineKeyboardButton(text="💰 Narxi", callback_data="narxi"))
                await bot.send_message(UserId, text=f"⚫️ Tanlagan mahsulotingiz: <b>{newsmall}</b> , Bo'limidan: <b>{oldsmallitem_keep}</b> \n \n Nimani o'zgartirmoqchisiz tanlang : " , reply_markup=newsmallmarkup,parse_mode="HTML")
          
          await Renamesmallmenuall.next()
          
          
          
async def newname_small_iteam_type(call: types.CallbackQuery, state: FSMContext):
      if f"{call.from_user.id}" == ID:
          UserId = call.from_user.id
          async with state.proxy() as data:
              data['item_type_keeper'] = call.data
          await bot.send_message(UserId,"Malumotni yuklang yoki yozing:")
          await Renamesmallmenuall.next()
async def item_keeper_of_type(message: types.Message, state: FSMContext):
          if f"{message.from_user.id}" == ID:
             UserId = message.from_user.id
             async with state.proxy() as data:
                data['text_or_file'] = message.text
             datalar = await state.get_data()
             conn.row_factory = sqlite3.Row
             d = conn.cursor()
    
             d.execute(f"""UPDATE '{datalar['oldsmallitem']}' SET '{datalar['item_type_keeper']}' = '{datalar['text_or_file']}' WHERE nomi = '{datalar['newsmallitem']}'""")
             conn.commit()
             await bot.send_message(UserId, text=f"Yangi ma'lumotlar saqlandi ✅ : \n \n pastda eski nomlari yana nimanidir o'zgartirmoqchi busangiz :", reply_markup=nav.bekor_qilish_menu)
        
             await state.finish()
            
                
                
                
                
                
                
                
async def bekor_qilish(callbacks: types.CallbackQuery, state: FSMContext):
      if f'{callbacks.from_user.id}' == ID:
           if callbacks.data == "bekor qilish menu":
              await state.finish()
              await bot.delete_message(callbacks.from_user.id,  callbacks.message.message_id)
              await bot.send_message(callbacks.from_user.id,"O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.uzgartiruvchilar)
           if callbacks.data == 'Bekor qilish small':
              await state.finish()
              await bot.delete_message(callbacks.from_user.id,  callbacks.message.message_id)
              await bot.send_message(callbacks.from_user.id,"O'zgartirmoqchi bulgan bulimizni tanlang ⬇️", reply_markup=nav.Smallmenuuzgartirish)


     
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
    
    dp.register_callback_query_handler(oldname_menu, state=Renamemenuall.oldmenurename)
    dp.register_message_handler(uzgartirish_menu_name, state=Renamemenuall.newnamemenu)
    dp.register_callback_query_handler(bekor_qilish, state="*",text=['bekor qilish menu', 'Bekor qilish small'])
    dp.register_callback_query_handler(bulim_joylash, state=FSMadmin.bulimjoylash)
    dp.register_callback_query_handler(delete_mahsulot, state=itemkeeper.delitemname)
    dp.register_callback_query_handler(pick_delete_item, state=itemkeeper.items)
    dp.register_callback_query_handler(rename_small_menu,state=Renamesmallmenuall.oldsmallitem)
    dp.register_callback_query_handler(newname_small_type_giver, state=Renamesmallmenuall.newsmallitem)
    dp.register_callback_query_handler(newname_small_iteam_type, state=Renamesmallmenuall.item_type_keeper)

    dp.register_message_handler(item_keeper_of_type, state=Renamesmallmenuall.text_or_file)
# for c in range(1,115):
      
  
#     if c < 31:
        
              
#                sura1.insert(InlineKeyboardButton(text=c, callback_data=f"sura3{c}"));    
    
    
    
    