# The-Teller-v1-WIP
A partially functioning WIP Discord deathroll bot with a fully working albeit unfair sqlalchemy banking system. Also features some smaller command such as an image upload and a random League of Legends champion selector for any League degenrates I may have the displeasure of meeting.

------------------------------------------------------------------
Command list:

b!balance: displays your balance. If you dont have a balance one will be given to you courtesy of the family

b!dr @challengee#0000 *amount*: requests a response from person you pinged and after receiving a response along the lines of b!dr @challenger#0001 *same amount* will start a deathroll. 

For more info on deathrolling: https://www.youtube.com/watch?v=HkWH5n2uFF8

b!league: says the name of a random League of Legends champ.

b!info: displays this info in the server you type this in provided the bot is there

b!ratcopter: eff around and find out

------------------------------------------------------------------
There are a lot of glitches with the deathrolling and banking system at the moment that I will most likely be working to fix on top of adding more gambling options. Blackjack coming real soon, possibly...

bank.py is a simple bank while sqlbank.py is that same bank integrated into sqlalchemy --a python library for sqlite.
