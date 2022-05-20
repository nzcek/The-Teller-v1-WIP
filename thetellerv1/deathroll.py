import random

def singleroll(max):
  return (random.randint(1,max))

def deathroll(number):
    x = 0
    rolls = []
    while number > 1:
        newnum = singleroll(number)
        print(newnum)
        number = newnum
        rolls.append(newnum)
        x += 1
        print("loop =" + str(x))
    return rolls



 	
 	
