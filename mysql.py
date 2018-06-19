import MySQLdb

db = MySQLdb.connect(host="ooza.co.ke",
                     user="oozacoke_python",
                     passwd="passwordforpython",
                     db="oozacoke_scratch",
                     port=3306)

print("database connection established")
db.query("""SELECT * FROM security""")
r = db.use_result()
print(r.fetch_row())
db.close()