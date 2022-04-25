#!/usr/bin/env python
#
# Created by Purplelemons-dev.
# Mon 11 Apr 2022 09:49:16 PM CDT
#

import random
from time import sleep

class Item:
    def __init__(self, name:str, description:str, canBeDropped:bool, damage=0, foodValue=0, price=0):
        self.name = name
        self.description = description
        self.canBeDropped = canBeDropped
        self.damage = damage
        self.foodValue = foodValue
        self.price = price
    
    def describe(self):
        description=f'Damage: {self.damage}\n' if self.damage > 0 else ''\
        f'Food Value: {self.foodValue}\n' if self.foodValue > 0 else ''\
        f'Price: {self.price}'
        print(f"{self.name}: {self.description}\n{description}")

    def special(self,player):
        pass


class Room:
    def __init__(self,name:str,description:str,entities:list,adjacentRooms=None,droppedItems:list[Item]=[]):
        self.name = name
        self.description = description
        self.entities:list[Entity] = entities
        self.droppedItems = droppedItems
        self.adjacentRooms:dict[str,Room] = adjacentRooms
        self.explored:bool = False


class Player:
    def __init__(self,name:str):
        self.name = name
        self.health = 100
        self.inventory:list[Item]=[]
        self.money=0
        self.weilding:Item=None
        self.currentRoom:Room=None
        self.lastMove:str=None
        self.fighting:Entity=None

    def actions(self,options:dict[str,]):
        print("\nWhat do you do?")
        for option in options:
            print(option)
        choice = input("> ").lower()
        if choice:
            for opt,func in options.items():
                if opt.startswith(choice[0]):
                    func()
                    return
        print("Invalid choice.")
        self.actions(options)
    
    def eat(self,itemName:str=None):
        if itemName is None:
            if not self.inventory:
                print("You don't have anything to eat.")
                return
            self.show_inventory()
            itemName=input("What do you want to eat? ")
        itemName=itemName.lower()
        for item in self.inventory:
            if item.name.lower().startswith(itemName) and item.foodValue > 0:
                self.health += item.foodValue
                print(f"You eat the {item.name} and gain {item.foodValue} health.")
                self.inventory.remove(item)
                return
        print("You can't eat that.")

    def change_room(self,direction:str=None):
        if direction is None:
            available_directions = ", ".join(d.upper() for d in self.currentRoom.adjacentRooms.keys())
            direction = input(f"Which direction do you want to go? ({available_directions}) ")
        direction = direction.lower()
        if direction in self.currentRoom.adjacentRooms:
            self.currentRoom = self.currentRoom.adjacentRooms[direction]
            self.lastMove = direction
            message=f"You go {self.prettify_direction(direction)}"
            if not self.currentRoom.explored:
                self.currentRoom.explored = True
                message+=f" and enter {self.currentRoom.description}"
            print(message+".")
            return
        print("You can't go that way.")

    def back(self):
        if self.lastMove is None:
            print("You can't go back from here.")
            return
        self.change_room(self.reverse_direction(self.lastMove))

    def reverse_direction(self,direction:str):
        return {
            'n':'s',
            's':'n',
            'e':'w',
            'w':'e'
        }[direction]

    def prettify_direction(self,direction:str):
        return {
            'n':'north',
            's':'south',
            'e':'east',
            'w':'west'
        }[direction]

    def equip(self,weapon:Item=None):
        if weapon is None and len([i for i in self.inventory if i.damage])==0:
            print("You don't have any weapons to equip.")
            return
        if weapon is None:
            items='\n'.join(item.name for item in self.inventory if item.damage>0)
            print(f"You have the following items:\n{items}")
            weapon = input("What do you want to equip? ")
        weapon = weapon.lower()
        for item in [i for i in self.inventory if i.damage>0]:
            if item.name.lower().startswith(weapon):
                self.weilding = item
                print(f"You equip the {item.name}.")
                return
        print("You can't equip that.")

    def attack(self):
        if self.weilding is None:
            self.weilding = Item('your fists', 'A pair of fists', False, 10)
        print(f"\nYou attack with {self.weilding.name}.")
        attack_modifier = random.random()
        if attack_modifier<.1:
            print("Your attack missed!")
        elif attack_modifier>.9:
            damage = self.weilding.damage*2
            self.fighting.health -= damage
            print(f"Your attack was SUPER EFFECTIVE, dealing {damage} points of damage!")
        else:
            damage = self.weilding.damage
            self.fighting.health -= damage
            print(f"You hit {self.fighting.name}, dealing {damage} points of damage!")
        print("\n")

    def combat(self):
        print(f"You are now fighting {self.fighting.name}.")
        round=0
        while self.fighting is not None:
            if round%2:
                # Enemy attacks on odd rounds
                self.fighting.attack(self)
                print(f"{self.fighting.name} has {self.fighting.health} health remaining.")
                print(f"You have {self.health} health remaining.")
            else:
                # Player attacks on even rounds
                self.actions({
                    "1. Attack":self.attack,
                    "2. Eat":self.eat,
                    "3. Equip":self.equip,
                })
            round+=1
            if self.health <= 0:
                break
            if self.fighting.health <= 0:
                dropped='\n - '.join(item.name for item in self.fighting.items)
                print(f"{self.fighting.name} dies and drops:\n - {dropped}")
                self.currentRoom.droppedItems+=self.fighting.items
                self.currentRoom.entities.remove(self.fighting)
                self.fighting = None
                break
            sleep(1)

    def buy(self,item:Item):
        if self.money >= item.price:
            self.money -= item.price
            self.inventory.append(item)
            print(f"You buy the {item.name} for {item.price} gold.")
        else:
            print("You can't afford that.")

    def sell(self,item:Item):
        if item in self.inventory:
            self.money += item.price
            self.inventory.remove(item)
            print(f"You sell the {item.name} for {item.price} gold.")
        else:
            print("You don't have that item.")

    def interact(self,object=None):
        if object is None:
            objectName = input("What do you want to interact with? ").lower()
        for entity in self.currentRoom.entities:
            if entity.name.lower().startswith(objectName):
                entity.special(self)
                return
        for item in self.inventory:
            if item.name.lower().startswith(objectName):
                item.describe()
                return
        for item in self.currentRoom.droppedItems:
            if item.name.lower().startswith(objectName):
                self.inventory.append(item)
                self.currentRoom.droppedItems.remove(item)
                print(f"You pick up the {item.name}.")
                return
        print("You can't interact with that.")

    def show_inventory(self):
        if self.inventory:
            items='\n'.join(item.name for item in self.inventory)
            print(f"You have the following items:\n{items}")
            return
        print("You don't have any items.")

    def show_room(self):
        print(f"You are in {self.currentRoom.description}.")
        if self.currentRoom.entities:
            entities='\n'.join(entity.name for entity in self.currentRoom.entities)
            print(f"You see the following creatures:\n{entities}")
        if self.currentRoom.droppedItems:
            items='\n'.join(item.name for item in self.currentRoom.droppedItems)
            print(f"You see the following items:\n{items}")

    def show_stats(self):
        print(f"{self.name}:")
        print(f"  Health: {self.health}")
        print(f"  Money: {self.money}")
        if self.weilding:
            print(f"\tWeapon: {self.weilding.name}, damage: {self.weilding.damage}")

    def show_surroundings(self):
        surroundings='\n'.join(f" - To the {self.prettify_direction(direction).title()} is a {room.name}" for direction,room in self.currentRoom.adjacentRooms.items())
        print(f"You can go to the following rooms:\n{surroundings}")

    def look(self,object=None):
        if object is None:
            self.actions({
                "1. Inventory":self.show_inventory,
                "2. Room":self.show_room,
                "3. Stats":self.show_stats,
                "4. Surroundings":self.show_surroundings,
            })
    
    def drop(self,item:Item):
        if item in self.inventory:
            self.inventory.remove(item)
            self.currentRoom.droppedItems.append(item)
            print(f"You drop the {item.name}.")
        else:
            print("You don't have that item.")


class Entity:
    # I'd like to make a boss subclass sometime in the future...
    def __init__(self,name:str,description:str,health:int,damage:int,items:list[Item]):
        self.name = name
        self.description = description
        self.health = health
        self.damage = damage
        self.items = items
        self.npc_phrases = [
            "I'm not sure what you're talking about.",
            "Hello there!",
            "Oh look at the time!",
            "Mighty fine weather we're having."
        ]
    
    def attack(self,player:Player):
        player.health -= self.damage
        print(f"{self.name} hit you, dealing {self.damage} points of damage!")
    
    def special(self,player:Player=None):
        if self.damage:
            player.fighting = self
            player.combat()
        else:
            self.talk(random.choice(self.npc_phrases))

    def talk(self,phrase:str):
        print(f"{self.name}: {phrase}")


class World:
    def __init__(self, start:Room):
        self.start = start
        self.start.explored = True
        self.player:Player = Player(
            input("What is your name? ")
        )
        self.player.currentRoom = start


def main():
    # Room creation. This could probably be improved by utilizing a map
    # so that each room has some ID on a 2D grid defined from the very
    # beginning.
    start=Room(
        name="Start",
        description="a wet and muddy ditch by the road.\nYou have no recollection of how you got here or where you are",
        entities=[]
    )
    bartender=Entity(
        name="Bartender",
        description="a weary, yet friendly looking fellow",
        health=100,
        damage=0,
        items=[
            Item(
                name="Beer",
                description="a foaming glass of beer",
                canBeDropped=True,
                foodValue=10,
                price=10,
            )
        ]
    )
    def bartender_kind(player:Player):
        bartender.talk("Welcome to the tavern!")
        print("The bartender greets you and offers you a beer.")
        player.inventory.append(bartender.items.pop())
        print("You received a beer!")
        # We dont want to give away infinite beer haha
        bartender.special=lambda:None
    bartender.special = bartender_kind
    tavern=Room(
        name="Tavern",
        description="a cozy tavern, bustling with other travelers",
        entities=[
            bartender
        ]
    )
    road=Room(
        name="Road",
        description="a dirt road leading to a small town",
        entities=[]
    )
    town=Room(
        name="Town",
        description="a small town, bustling with people",
        entities=[]
    )
    dungeon=Room(
        name="Dungeon",
        description="a dark, damp dungeon, something is moving in the corner",
        entities=[
            Entity(
                name="Zombie",
                description="a rotting corpse, emitting a foul stench",
                health=25,
                damage=10,
                items=[
                    Item(
                        name="Claw",
                        description="a splintered, rotting hand",
                        canBeDropped=True,
                        damage=15,
                        price=1
                    )
                ]
            )
        ]
    )

    # Room linking
    start.adjacentRooms = {
        'n':tavern,
        'e':road,
    }
    tavern.adjacentRooms = {
        's':start,
    }
    road.adjacentRooms = {
        'w':start,
        'e':town,
        's':dungeon
    }
    town.adjacentRooms = {
        'w':road
    }
    dungeon.adjacentRooms = {
        'n':road
    }


    # This is the main game loop
    world=World(start)
    print(f"You are in {world.start.description}.")
    try:
        while world.player.health > 0:
            world.player.actions({
                "1. Go":world.player.change_room,
                "2. Interact":world.player.interact,
                "3. Look":world.player.look,
                "4. Back":world.player.back,
                "5. Eat":world.player.eat,
                "6. Equip":world.player.equip
            })
        print("You died.")
    except KeyboardInterrupt:
        print("\nYou quit.")

    print(f"Thanks for playing, {world.player.name}!")


if __name__ == '__main__': main()
