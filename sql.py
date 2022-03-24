#Siin on SQL db kood
import sqlite3

ühendus = sqlite3.connect('KVdb.db')
c = ühendus.cursor()
c.execute("SELECT * FROM Mustamäe")

#c.execute("INSERT INTO Mustamäe (*) VALUES (*)")


c.close()

ühendus.commit()

ühendus.close()
