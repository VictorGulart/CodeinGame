import sys
import math
import operator

''' 
Help Debugging
Write an action using print
To debug: print("Debug messages...", file=sys.stderr, flush=True)


1st idea: get the most expensive brew that i can make

'''

class Witch():

    ''' 
    Orders information:
      action_id: the unique ID of this spell or recipe
      action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
      delta_0: tier-0 ingredient change
      delta_1: tier-1 ingredient change
      delta_2: tier-2 ingredient change
      delta_3: tier-3 ingredient change
      price: the price in rupees if this is a potion
      
      tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax; For brews, this is the value of the current urgency bonus
      
      tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell; For brews, this is how many times you can still gain an urgency bonus
      castable: in the first league: always 0; later: 1 if this is a castable player spell
      repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell 
    Action info:
      in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT

    List:
        1st idea get the most expensive brew and return the move
        2nd idea get the most expensive brew with the least number of 
            rounds needed to complete it ( similiar a ROI, kinda ) 

    Ideas:
        How not to search for the same spells all the time (maybe adding a queue)


        '''

    def __init__(self):
        # Stores number corresponding to qty of each item
        self.inventory = list()
    
        # Each item is an object - Order() 
        self.orders = dict() 

        # Book of spells
        self.book = dict()

        # Score
        self.score = 0

        # Enemy info
        self.enemy_score = 0
        self.enemy_inventory = list()

        # Target Brew
        self.target = None
        
        # Moves (find a way to hold only available moves)
        self.queue_moves = list() # NOT IN USE 
        
        # Previous Move
        self.prev_move = None # to check if it was a brew to clear target

        # Missing ingredients list
        self.missing = []


    def __str__( self ):
        books = ", ".join( [ spell.spell_ID for spell in self.book.values() ] )
        return f'{books}'

    def set_count( self ):
        ''' Number of orders '''
        self.count = len(orders)

    def add_order(self, id, price, *ingredients):
        ''' Add to the dictionary orders a new order object '''

        ## Check if the order is already in the queue
        if not self.orders.get(id):
           self.orders[id] = Order(id, price, *ingredients)

    def add_spell( self, id, castable, *ingredients):
        ''' Add to the dictionary book a new spell object '''

        # Check if the spell is already in the book
        if not self.book.get(id):
            self.book[id] = Spell(id, castable, *ingredients)

        # Set the castable option - update 
        else:
            self.book[id].set_castable(castable)

    
    def add_inv_score( self, score, inv ):
        ''' Saves the score and inventory '''
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        self.score = score
        self.inventory = list( map( int, inv ) )

    def enemy_inv_score( self, score, inv ):
        ''' Saves the enemy score and inventory '''
        self.enemy_score = score 
        self.enemy_inventory = list( map( int, inv ) )

   def first_tactic( self ):
        ''' This is taking the decision on which brew to make 
            and removes the order decided from the orders dict 

            Return a move
        '''
        target = self.get_most_expesive()
        self.remove_order(target)

        return f'BREW {id}' 

    def second_tactic( self ):
        ''' Gets the most expensive brew and cast until have enough
            ingredients for it and so on 
            
        Steps:
            
            1- Get most expensive brew
            2- Get missing ingredients list (example [0,0,0,-1])

            ???? Enter a loop to find the spells needed ???? 
            3- Get spells from the book based on missing items
            4- Check all the spells to get one that can be cast
                if yes cast, else carry on 
            At this point there are 2 options
                a) the are no spells,
                    5- Rest
                b) there are spells but can not be cast (missing ingredients)
                    then go to step 5
                     
            5- add the cost of the spell to the missing list, this way the list
                will show another item actually missing.
            
        '''

        # Get most expensive brew
        if ( self.target == None):
            self.target = self.get_most_expesive()
            print(f'Target { self.target }', file=sys.stderr, flush=True)

        ## Check if there enough ingredients for the brew
        self.missing = self.missing_ingredients(self.target) 
        ## print(f'Missing values { missing }', file=sys.stderr, flush=True)
        
        # If there is nothing missing, Brew it 
        if not any( self.missing ):
            self.remove_order(self.target)
            tmp_id = self.target
            self.target = None
            return f'BREW { tmp_id }'

        counter = 0
        ## Get correct spell to cast 
        while True:
            counter += 1 

            # Get the spells
            spells = self.search_book( self.missing ) 

            # If there are no spells available to cast 
            # ( all exhausted or can't have any items )
            if not spells:
                return f'REST'

            # Special case, 1 spell - castable, cost is missing, not available
            if len(spells) == 1:
                if any( map( lambda x,y: True if x<0 and y<0 else False, self.missing, self.book[spells[0]].spell_cost ) ):
                    return f'REST'

            # Search all spells for a castable or add the cost to missing list
            for spell_ID in spells:
                if self.book[ spells[0] ].isAvailable(self.inventory):
                    # yes then break and cast
                    return f'CAST { spell_ID }'
                else:
                    # numpy can be used to help speed up if needed
                    self.book[spells[0]].set_castable(False)
                    self.missing = list( map( operator.add, 
                                         self.missing, 
                                         self.book[ spells[0] ].spell_cost ) ) 
    def third_tactic(self):
        ''' Get the best brew giving the most rupees for less rounds '''
        pass


    def get_best_brew( self ):
        ''' Returns the best brew to target '''
        pass



    def missing_ingredients( self, id_target ):
        ''' Returns a list of the number of items missing
            If missing appends the difference, if nothing is missing 
            then append 0, cause nothing is needed.

            id_target - is the potion to be brewed

        Example:
            potion = [-2,-1,0,-1]
            inventory = [3,0,0,0]
            missing = [0,-1,0,-1]

        '''

        missing = list()
        
        for idx in range(len(self.inventory)):
            diff = self.inventory[idx] + self.orders[id_target].ingredients[idx]
            if diff < 0:
                missing.append(diff)
            else:
                missing.append(0)

        return missing


    def search_book( self, missing ):
        ''' Returns a list of available (not exhausted) spells that return the 
            desired ingredients '''

        # List of possible spells to cast 
        spells = list()

        for spell in self.book.values():
            ## print(spell, file=sys.stderr, flush=True )
            related = any( map( self.are_related, missing, spell.spell_return ) ) 

            if related and (spell.isCastable()):
                # if the spell returns at least one of the ingredients needed
                spells.append(spell.get_id())

        return spells
            
    def are_related(self, item_missing, spell_return):
        ''' Returns True if both values are different from 0, 
            meaning the spell will return at least one unit of this
            ingredient 
        '''

        if item_missing != 0 and spell_return != 0:
            return True
        else:
            return False
        

    def any_missing( self, id ):
        ##
        #
        # NOT IN USE 
        #
        ##
        ''' Returns False if the ingredients in the inventory are enough
            to BREW the potion, the ingredient index otherwise 
            
            id is from the recipe
        '''

        for idx in range(3,-1,-1):

            # if inventory + (-qty ingredient needed)
            if self.get_item_count(idx) + self.orders[id].ingredients[idx] < 0:
                # The witch need to cast more spells to get the item
                return idx

        return False # There are enough ingredients in inventory
    
    
    def get_item_count( self, idx):
        ''' Just return the count of a certain ingredient in stock '''
        return self.inventory[idx]


    def remove_order( self, order_ID ):
        ''' Deletes the order from the dictionary '''
        del self.orders[order_ID]

    def use_spell( self, spell_ID ):
        ''' To use the spell, and change the castable property '''
        self.book[spell_ID].use()

    def get_most_expesive( self ):
        ''' Get the mos expensive brew and if there is a match return 
        the one with less ingridients needed '''
        brew_ID = int
        price = 0 

        # Remeber orders is a dictionary

        for id_dict, order in self.orders.items():
            if order.price > price:
                brew_ID = id_dict 
                price = order.price

            elif order.price == price:
                # one that has a greater value
                # cause they have negative values meaning
                # the loss of ingredients 

                # If the old order represents a bigger loss than change
                if sum(self.orders[brew_ID].ingredients) < sum(order.ingredients):
                    brew_ID = id_dict
                    price = order.price
        return brew_ID

    def classify_spells( self ):
        ''' Will be a dictionary containing with each key with a list as value.
            This list will be a full of spells that return at least 1 of the
            specic ingredient '''

        # Creates an dictionaty with the amount of entries equal to the len
            # of the book dictionary
        self.categories = {key:list() for i in range(len(self.book))} 
        pass
    


class Order():
    def __init__( self, order_ID=None, price=0, *ingredients ):
        ''' Create an order with its particular values '''
        self.order_ID = int( order_ID )
        self.price = int( price )
        self.ingredients = list( map( int, ingredients ) )

    def __str__( self ):
        return f'Order {self.order_ID},m ${self.price}, n{self.ingredients}'


class Spell():
    def __init__( self, spell_ID, castable, *recipe ):
        ''' Creates a spell with its particular values '''
        self.spell_ID = spell_ID
        self.castable = int( castable )
        self.recipe = list( map( int, recipe ) ) # includes cost and target
        self.spell_cost = list()
        self.spell_return = list()


        # Set cost and target of the spell
        self.set_cost()
        self.set_return()

    def __str__( self ):
        return f'Spell {self.spell_ID} is castable {self.isCastable()}'


    def get_id( self ):
        ''' Returns the ID value '''
        return self.spell_ID

    def set_castable( self, castable ):
        ''' Set castable value '''
        self.castable = int ( castable )

    def isCastable( self ):
        ''' Returns True if Castable False otherwise '''
        if (self.castable):
            return True
        else: 
            return False

    def isAvailable( self, inventory):
        ''' Returns True if there are enough ingredients to cast it,
            otherwise returns False '''
        
        # Base case the spell costs nothing
        if sum(self.spell_cost) == 0:
            return True

        for idx, val in enumerate( self.recipe ):
            # if the inventory - cast cost is less than 0 
            if inventory[idx] + val < 0:
                return False
        return True
            

    def set_return( self ):
        ''' The list target holds the amount of ingridients the spell returns '''
        self.spell_return = [ val if val > 0 else 0 for val in self.recipe ]


    def set_cost( self ):
        ''' The list cost represent which ingridients are use to cast the spell '''
        self.spell_cost = [val if val < 0 else 0 for val in self.recipe ]



# Instantiate the witch
witch = Witch()


# GAME LOOP
while True:

    action_count = int(input())  # the number of spells and recipes in play


    ## Gathering all the data
    for i in range(action_count):
        
        action_id, action_type, d0, d1, d2, d3, price, tome_index, tax_count, castable, repeatable = input().split()


        # If this is an order
        if action_type == 'BREW':
            ## Add the order to witch's list
            witch.add_order( action_id, price, d0, d1, d2, d3 )

        # If it it a spell
        elif action_type == "CAST": 
            witch.add_spell(action_id, castable, repeatable, d0, d1, d2, d3 )

        # Opponent's Information
        elif action_type == "OPPONENT_CAST":
            pass

        # Spells Available to learn
        elif action_type == "LEARN":
            # tax_count is the amount of t0 ingredients won as bonus, or 0
            witch.add_tome_spell( tome_index, ) 

        # ignore these values
        witch.extra_info(tome_index, tax_count)


    ## Getting the inventory
    for i in range(2):
        # [item1, item2, item3, item4, score]
        values = [int(j) for j in input().split()]
        if i == 0:
            witch.add_inv_score( values[-1], values[:-1] )
        else:
            witch.enemy_inv_score( values[-1], values[:-1] )

    ## Get the most expensive brew
    ## move = witch.first_tactic()
    ## print( f'The most expensive {move}', file=sys.stderr, flush=True )

    ## Get the most expensive brew but cast the spell most 
    ## expensive (time) as well
    move = witch.second_tactic()
    print( "Inventory ", witch.inventory, file=sys.stderr, flush=True )
    print( "Missing ", witch.missing, file=sys.stderr, flush=True )

    print(move)




