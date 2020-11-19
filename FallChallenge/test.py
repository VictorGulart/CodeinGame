import numpy as np

inv = [3,0,0,0]

spells = [ [2,0,0,0],
           [-1,1,0,0],
           [0,-1,1,0],
           [0,0,-1,1] ]

potion = [0,-3,-2,0]

rest = [0,0,0,0]


inv = np.array( inv )
spells = np.array( spells )
potion = np.array( potion )
rest = np.array( rest )

# Default values
# print(inv)
# print(spells)
# print(potion)

print(" Inventory + Potion ", inv + potion )
print( inv + spells[1:] )
print(inv + spells.sum(axis=1) )
