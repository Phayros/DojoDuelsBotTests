from tinydb import TinyDB, Query

Duelist_db = TinyDB("DuelistData.json")
User_db = TinyDB("UserData.json")

User1 = {
    "Id": "phayros",
    "Achievements": {
        "Demonstration Hell": "Have a duelist without a demo for over a year",
        "Faction Member": "Have at least one duelist in a faction"
    },
    "Duelists": ["Phayros", "Runic"],
    "Duelist_ids": [1,2],
    "Cierites": {
        "MA": [0,0],
        "FR": [0,0],
        "ST": [0,0],
        "IS": [0,0],
        "GZ": [0,0],
        "CE": [0,0],
        "GM": [0,0],
        "AL": [0,0],
        "Jewels": 0,
        "Radiant": 0
    }
}

Duelist1 = {
    "Name": "Phayros",
    "Duelist_id": 1,
    "Creator": "phayros",
    "Icon": "https://f2.toyhou.se/file/f2-toyhou-se/characters/17064943?1718036644",
    "Thread": "https://discord.com/channels/108249481656418304/1223293645080236042",
    "Information": "Phayros is a creative spirit full of curiosity and wonder that wants to travel around the world and learn about the magic and the people.",
    "Gelta": 500,
    "Medium": {
        "Animated": True,
        "Comic": True,
        "Written": True
    },
    "Win_Loss_Tie": [0,0,0]
}

Duelist2 = {
    "Name": "Runic",
    "Duelist_id": 2,
    "Creator": "phayros",
    "Icon": "https://f2.toyhou.se/file/f2-toyhou-se/characters/17843172?1662253664",
    "Thread": False,
    "Information": "Runic is a robot lich that is in a constant internal battle between fighting her past and joining him.",
    "Gelta": 0,
    "Medium": {
        "Animated": True,
        "Comic": False,
        "Written": False
    },
    "Win_Loss_Tie": [0,0,0]
}

User2 = {
    "Id": "corvidcreek",
    "Achievements": {
        "An IQ too High?": "You wouldn't understand",
        "Experienced Duelist": "Have a total count of over 10 duels over all your duelists"
    },
    "Duelists": ["BHOP", "Ryobu"],
    "Cierites": {
        "MA": [0,0],
        "FR": [0,0],
        "ST": [0,0],
        "IS": [0,0],
        "GZ": [0,0],
        "CE": [0,0],
        "GM": [0,0],
        "AL": [0,0],
        "Jewels": 0,
        "Radiant": 0
    }
}

Duelist3 = {
    "Name": "BHOP",
    "Duelist_id": 3,
    "Creator": "corvidcreek",
    "Icon": False,
    "Thread": "https://discord.com/channels/108249481656418304/1385975535515205712",
    "Information": "Explosion rabbit that bhops",
    "Gelta": 1000,
    "Medium": {
        "Animated": True,
        "Comic": True,
        "Written": False
    },
    "Win_Loss_Tie": [2,1,0]
}

Duelist4 = {
    "Name": "Ryobu",
    "Duelist_id": 4,
    "Creator": "corvidcreek",
    "Icon": False,
    "Thread": "https://discord.com/channels/108249481656418304/1271162755319332975",
    "Information": "demon gunner, speedster bounty hunter",
    "Gelta": 1500,
    "Medium": {
        "Animated": True,
        "Comic": True,
        "Written": False
    },
    "Win_Loss_Tie": [5,2,0]
}

User_db.insert(User1)
User_db.insert(User2)
Duelist_db.insert(Duelist1)
Duelist_db.insert(Duelist2)
Duelist_db.insert(Duelist3)
Duelist_db.insert(Duelist4)