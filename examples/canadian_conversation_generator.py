"""
The expected result of running this script is an endless stream of

I'm not your buddy, friend!
He's not your friend, pal!
I'm not your pal, buddy!
He's not your buddy, friend!
I'm not your friend, pal!
He's not your pal, buddy!
I'm not your buddy, friend!
He's not your friend, pal!
"""

from time import sleep
from itertools import cycle                 
from slinkie import Slinkie                 

canadian = cycle(('buddy', 'friend', 'pal'))

who = cycle(("I'm", "He's"))

conversation = (
    Slinkie(canadian)
        .sweep(2)
        .map(lambda it: f"{next(who)} not your {it[0]}, {it[1]}!"))

while True:
    print(next(conversation))
    sleep(1)
