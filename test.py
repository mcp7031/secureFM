import random
import locations

def isEveryOther(time):
    return (random.randrange(1,100) % time == 0)

print (isEveryOther(3))
print (random.choice(list(locations.LOC)))
