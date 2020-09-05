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
import sys
from Core.enigma_machine import *
from Core.version import VERSION
from Core.rotor_factory import RotorFactory
from Core.reflector_factory import ReflectorFactory
from Core.rotor_contact import RotorContact

# https://cryptii.com/enigma-machine
# AAAA with positions 2,3,21 should return MKIEY


RotorPosition_One = 0
RotorPosition_Two = 1
RotorPosition_Three = 2


def main():
    print("Electronic Enigma Core Version V{0}".format(VERSION))
    print("Copyright (C) 2015-2018 Electronic Engima Development Team")

    try:
        enigma_machine = EnigmaMachine('Enigma1')

    except ValueError as err:
        print(f'[ERROR] {err}')
        return

    config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

    if not config_return:
        print(f'[ERROR] {enigma_machine.last_error}')
        return

    enigma_machine.debug_messages = True

    # Set the rotor positions
    enigma_machine.SetRotorPosition(RotorPosition_One, 2)
    enigma_machine.SetRotorPosition(RotorPosition_Two, 3)
    enigma_machine.SetRotorPosition(RotorPosition_Three, 21)

    # machine.GetRotor(0).RingSetting = 2
    # machine.GetRotor(1).RingSetting = 2
    # machine.GetRotor(2).RingSetting = 2

    string_to_encode = "AAAAA"
    print(f"String to encode : {string_to_encode}")

    encrypted = ""
    for character in string_to_encode.upper():
        if character >= 'A' and character <= 'Z':
            character = RotorContact[character]
            encrypted_letter = enigma_machine.PressKey(character)
            print(f'Encrypted {character} as {encrypted_letter}')
            encrypted += str(enigma_machine.PressKey(character).name)

    print("Encrypted : {0}".format(encrypted))


if __name__ == '__main__':
    main()
