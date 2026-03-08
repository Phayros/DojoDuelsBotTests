from tinydb import TinyDB, Query

Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")

User = Query()

all_duelists = Duelist_db.all()
print("All duelists: ", all_duelists)

all_users = User_db.all()
print("All users: ", all_users)