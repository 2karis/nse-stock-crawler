import MySQLdb

db = MySQLdb.connect(host="88.99.93.223",
                     user="oozacoke_admin",
                     passwd="zCcnOhdZA8XS",
                     db="oozacoke_scratch",
                     port=3306)

print("database connection established")
db.query("""SELECT * FROM security""")
r = db.use_result()
print(r.fetch_row())
db.close()