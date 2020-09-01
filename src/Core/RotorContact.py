'''
    <one line to give the program's name and a brief idea of what it does.>
    Copyright (C) 2015-2020 Engima Simulator Development Team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''
from Singleton import Singleton


# ***********************************************************************
# Enumeration for converting a rotor pin/contact to a letter
# ***********************************************************************
@Singleton
class RotorContact(object):

    # Number of rotor contacts.
    NUMBER_OF_CONTACTS = 26

    # ASCII to contact offset value
    ASCII_TO_CONTACT_OFFSET = 64


    ##
    # Class initialisation.  Create the contacts dictionary.
    # @param self The object pointer.
    def __init__(self):
        self.__contact = {
             1 : 'A',
             2 : 'B',
             3 : 'C',
             4 : 'D',
             5 : 'E',
             6 : 'F',
             7 : 'G',
             8 : 'H',
             9 : 'I',
            10 : 'J',
            11 : 'K',
            12 : 'L',
            13 : 'M',
            14 : 'N',
            15 : 'O', 
            16 : 'P',
            17 : 'Q',
            18 : 'R',
            19 : 'S',
            20 : 'T',
            21 : 'U',
            22 : 'V',
            23 : 'W',
            24 : 'X',
            25 : 'Y',
            26 : 'Z'
        }


    ##
    # Convert a character [A-Za-z] to it's contact number.  If the parameter
    # 'character' is not a string of 1 character then a ValueErrorn exception
    # is generated.
    # @param self The object pointer.
    # @param character Character to convert to a contact number.
    # @return Success = Contact number [1-26] or ValueError exception.
    def CharacterToContact(self, character):
        # Verify that the character parameter is of type 'string'.
        if type(character) != str:
            raise ValueError("character is not a string")

        # Character has to be a single character, nothing more or less.
        if len(character) != 1:
            raise ValueError("character is more than one character!")

        # Get the integer ordinal of a one-character string and convert it to
        # a key (1 .. 26).
        asciiValue = ord(character.upper())
        contactNo = asciiValue - self.ASCII_TO_CONTACT_OFFSET

        # Verify contact is somewhere between 1 and max contact number.
        if (contactNo < 1) or (contactNo > self.NUMBER_OF_CONTACTS):
            raise ValueError("invalid contact number")

        # Return the contact number.
        return contactNo


    ##
    # Convert a contact number to a character [A-Za-z].
    # @param contact Contact number to convert to a character.
    # @return Success = character or ValueError exception.
    def ContactToCharacter(self, contact):
        # Verify that the contact is of type 'int'.
        if type(contact) != int:
            raise ValueError("Contact number is not an integer")

        if (contact < 1) or (contact > self.NUMBER_OF_CONTACTS):
            raise ValueError("invalid contact value")

        # Convert contact to ascii value then return character.
        asciiVal = contact + self.ASCII_TO_CONTACT_OFFSET
        return str(unichr(asciiVal))
