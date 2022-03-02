from cgitb import text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton as InlB, InlineKeyboardMarkup as InlM, callback_game, inline_keyboard


#Menu o'zgartirish uchun buttanlar
#IinlB == InlineKeyboardButton ga
#InlM == InlineKeyboardMarkup ga

AsosiyUzgartiruvchiButtonlar = ['Bosh menu', 'Mahsulotni uzgartirish']
uzgartiruvchilar = InlM(row_width=1)
bekor_qilish_menu = InlM(row_width=1).add(InlB(text="❌ Bekor qilish", callback_data="bekor qilish menu"))
Menuuzgartirish = InlM(row_width=1).add(InlB(text="➕ Menu qo'shish", callback_data="Menu qushish"),
    InlB(text="➖ Menu o'chirish",callback_data="Menu uchirish"),
     InlB(text="♻️ Menu o'zgartirsh", callback_data="menu uzgartirish"),
     InlB(text="❌ Bekor qilish",callback_data="bekor qilish menu")
    
    )
Smallmenuuzgartirish = InlM(row_width=1).add(InlB(text="➕ Smallmenu qo'shish", callback_data="smallmenu qushish"),
    InlB(text="➖ Smallmenu o'chirish",callback_data="smallmenu uchirish"),
     InlB(text="♻️ Smallmenu o'zgartirsh", callback_data="smallmenu uzgartirish"),
     InlB(text="❌ Bekor qilish",callback_data="bekor qilish menu")
    
    ) 
for n in AsosiyUzgartiruvchiButtonlar:
         uzgartiruvchilar.insert(InlB(text=n,callback_data=n))
         

         