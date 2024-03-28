# There have been a breakout of lassa fever, the population data is given below
people = [
    {"id": 1, "bg": "O+", "name": "micheal jackson"},
    {"id": 2, "bg": "O-", "name": "billy graham"},
    {"id": 3, "bg": "O+", "name": "arthur pendragon"},
    {"id": 4, "bg": "O+", "name": "elon musk"},
    {"id": 5, "bg": "O-", "name": "mark peterson"},
    {"id": 6, "bg": "O+", "name": "richard cypher"},
    {"id": 7, "bg": "O-", "name": "dora akunyili"},
    {"id": 8, "bg": "O+", "name": "mary slessor"},
    {"id": 9, "bg": "O+", "name": "ramsey now"},
    {"id": 10, "bg": "O-", "name": "anthony joshua"},
    {"id": 11, "bg": "O+", "name": "jack bauer"},
    {"id": 12, "bg": "O-", "name": "gabriel jesus"},
]


friendship_pair = [
    (1, 2), (1, 3), (1, 5), (2, 5), (2, 8), (3, 12), (3, 9), (4, 7), (5, 11), (6, 9), (10, 8)
]


# if one random person in the community gets infected, using the following assumptions,
# write a code that will give the following details

"""ASSUMPTIONS:
1.  All direct friends visit each other once a day
2.  Contact between an infected and non infected person leads to transmission of infection
3.  Disease Last for exactly 1 Day for O+ and 2 days for O- blood group
4.  Cured Persons can get infected 2 days after recovery
"""

"""TASK:
1.  Using a random Person as the first to be infected on day 0, write a code that give the following info:
    i.  Will everyone be cured? if so, after how many days?
    ii. Will everyone ever get infected at same time? if so, after how many days?
    iii. Who (or which people) gets infected last?
    
2.  Which Person or group of persons has worst and least effect respectively if they are first to get infected

3. Extract any other relevant data that might be helpful
"""

"""HINT:
    To choose a random person, use the code below
    import random
    random_person = random.sequence(people)
    
    this returns a random dictionary in the people list
"""