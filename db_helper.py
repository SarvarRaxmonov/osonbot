import sqlite3

conn = sqlite3.connect('oson.db')

c = conn.cursor()


#c.execute("CREATE TABLE asosiymenu(mainproductslist text)")
def MainButtonAdd(buttonname):

      return c.execute("INSERT INTO asosiymenu VALUES(?)",(buttonname,))
   


conn.commit()
