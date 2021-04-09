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
from simulation.enigma_machine import EnigmaMachine
from simulation.version import VERSION
from simulation.rotor_contact import RotorContact

# https://cryptii.com/enigma-machine
# AAAA with positions 2,3,21 should return MKIEY


ROTORPOSITION_ONE = 0
ROTORPOSITION_TWO = 1
ROTORPOSITION_THREE = 2

def encode_message(original_message, machine):
    encoded_message = []

    for character in original_message.upper():
        if character < 'A' or character > 'Z':
            print(f"[ERROR] Character '{character}' is invalid!")
            sys.exit()

        character = RotorContact[character]
        encoded_character = machine.press_key(character)
        encoded_message.append(encoded_character.name)

    encoded_str = "".join(encoded_message)
    return encoded_str


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

    #enigma_machine.debug_messages = True

    # # Set the rotor positions
    # enigma_machine.set_rotor_position(ROTORPOSITION_ONE, 1)
    # enigma_machine.set_rotor_position(ROTORPOSITION_TWO, 1)
    # enigma_machine.set_rotor_position(ROTORPOSITION_THREE, 1)

    # # machine.GetRotor(0).RingSetting = 2
    # # machine.GetRotor(1).RingSetting = 2
    # # machine.GetRotor(2).RingSetting = 2

    # string_to_encode = "AAAAA"
    # encoded = encode_message(string_to_encode, enigma_machine)
    # print("+----------------------------------------------")
    # print(f"Encoded string '{string_to_encode} as : {encoded}")
    # print(f"=> Rotor 1 Position: {enigma_machine.get_rotor_position(0)}")
    # print(f"=> Rotor 2 Position: {enigma_machine.get_rotor_position(1)}")
    # print(f"=> Rotor 3 Position: {enigma_machine.get_rotor_position(2)}")
    # print("+----------------------------------------------")

    # AAAA with positions 2,3,21 should return MKIEY

    # Set the rotor positions
    enigma_machine.set_rotor_position(ROTORPOSITION_ONE, 2)
    enigma_machine.set_rotor_position(ROTORPOSITION_TWO, 3)
    enigma_machine.set_rotor_position(ROTORPOSITION_THREE, 21)

    enigma_machine.set_rotor_position(ROTORPOSITION_ONE, 0)
    enigma_machine.set_rotor_position(ROTORPOSITION_TWO, 0)
    enigma_machine.set_rotor_position(ROTORPOSITION_THREE, 0)
    #enigma_machine.set_rotor_position(ROTORPOSITION_THREE, RotorContact.U.value)

    string_to_encode = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    encoded = encode_message(string_to_encode, enigma_machine)
    print("+----------------------------------------------")
    print(f"Encoded string '{string_to_encode} as : {encoded}")
    print(f"=> Rotor 1 Position: {RotorContact(enigma_machine.get_rotor_position(0)).name}")
    print(f"=> Rotor 2 Position: {RotorContact(enigma_machine.get_rotor_position(1)).name}")
    print(f"=> Rotor 3 Position: {RotorContact(enigma_machine.get_rotor_position(2)).name}")
    print("+----------------------------------------------")

    enigma_machine.set_rotor_position(ROTORPOSITION_ONE, RotorContact(2).value)
    enigma_machine.set_rotor_position(ROTORPOSITION_TWO, RotorContact(3).value)
    enigma_machine.set_rotor_position(ROTORPOSITION_THREE, RotorContact(21).value)

    string_to_encode = "AAAA"
    encoded = encode_message(string_to_encode, enigma_machine)
    print(f"Encoded string '{string_to_encode} as : {encoded}")


if __name__ == '__main__':
    main()
