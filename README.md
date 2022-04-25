# Dungeon Quest


## Table of Contents


* [Introduction](#introduction)
* [World](#world)
* [Items](#items)
* [Rooms](#rooms)
* [Entities](#entities)
* [Game Over](#game-over)


## Introduction

This game was programmed in just about two weeks, and I hope you enjoy it.
I also used GitHub Copilot to help me with the project, I suggest you get
on the waitlist as soon as you can!

This is a basic text-based dungeon game with several types of data structures
such as Items, Rooms, and Entities. Rooms are linked together by use of the
adjacentRooms dictionary which translates the cardinal directions to Room objects.

The [player](#player) can have a simple fight with an entity by using the combat() method.


## World

This class doesn't do much at the moment, but it can be used to handle game saves
and loading. It could also be used to handle the generation of the world (with a
`.generate()` method). This class also gets the name of the player.


## Player


The player is the main character of the game, controlled by 6 different inputs:

 1. Go
 2. Interact
 3. Look
 4. Back
 5. Eat
 6. Equip

The Interact action will allow the user to trigger the `.special()` method for various
objects in the room, including entities, dropped items, and items in the player's
inventory. The Look action will allow the user to view their inventory, the room,
the player's stats, and the surrounding area outside the room. The Back action will
return the player to the previous room (provided that is possible, currently the
only time this is prohibited is at the very beggining of the game, but I imagine that
the back action could be blocked if the world is broken up into acts or the player
enters a locked dungeon).


## Items


Items can be either food, weapons, or cosmetic. Damaging items are able to be equipped
either before or during combat. Food items are able to be eaten, and cosmetic items
are just for decoration or fun, having neither a food nor damage value.


## Rooms


Rooms are the basic building blocks of the game. They can be connected to other rooms
via the `.adjacentRooms` property, and can have items and entities in them. The rooms
also handle dropped items. I'd like to see a `.special()` method for rooms that can
be triggered by bringing some costmetic or weapon item to the room for an easter egg
or something.


## Entities


Entities are referred to as "creatures" in the game and can be either friendly or hostile
(based on wether their `.special()` method triggers the player's `.combat()` method or
not). The `.special()` method can be modified, as seen with the Bartender, to do different
things. 


## Game Over


This is where the game ends. The player can either die, win, or quit. Right now, the main
loop checks for the player's health and handles keyboard interupts, but player health and
winning can be moved to [`World`](#world).
