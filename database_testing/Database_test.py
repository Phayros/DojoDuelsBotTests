from tinydb import TinyDB, Query

Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")

User = Query()

# all_duelists = Duelist_db.all()
# print("All duelists: ", all_duelists)

# all_users = User_db.all()
# print("All users: ", all_users)

all_duelists = Duelist_db.all()

search= "p"
list=[]
for each in all_duelists:
    if search in each["Name"]:
        list.append(each)
if not list:
    print("no match")
else:
    for each in list:
        print(each["Name"])