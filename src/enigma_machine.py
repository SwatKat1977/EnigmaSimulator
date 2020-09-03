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
from Core.EnigmaMachine import *
from Core.MachineSetup import *
from Core.Version import *
from Core.RotorFactory import RotorFactory
from Core.ReflectorFactory import reflectorFactory
from Core.RotorContact import RotorContact

# https://cryptii.com/enigma-machine
# AAAA with positions 2,3,21 should return MKIEY


print("Electronic Enigma Core Version V{0}".format(ElectronicEnigmaVersion))
print("Copyright (C) 2015-2018 Electronic Engima Development Team")

# Read rotors XML file.
rotors, status = RotorFactory.Instance().CreateFromXML('../Data/rotors.xml')
if rotors == None:
    print("ERROR : Unable to read rotors XML file: {0}".format(status))
    sys.exit()

# Read reflectors XML file.
reflectors, status = reflectorFactory.CreateFromXML('../Data/reflectors.xml')
if reflectors == None:
    print("ERROR : Unable to read reflectors XML file: {0}".format(status))
    sys.exit()

# Create machine setup.
setup = MachineSetup(EnigmaModel.Enigma1, ["Rotor I", "Rotor II", "Rotor III"])

# Create Enigma machine.
machine = EnigmaMachine(setup, rotors, reflectors['Wide Reflector B'], True)

# Set the rotor positions
machine.SetRotorPosition(RotorPosition.One, 2)
machine.SetRotorPosition(RotorPosition.Two, 3)
machine.SetRotorPosition(RotorPosition.Three, 21)

# machine.GetRotor(0).RingSetting = 2
# machine.GetRotor(1).RingSetting = 2
# machine.GetRotor(2).RingSetting = 2

strToEncode = "AAAAA"
print("String to encode : {0}".format(strToEncode))

encrypted = ""
for char in strToEncode.upper():
    if char >= 'A' and char <= 'Z':
        char = RotorContact.Instance().CharacterToContact(char)
        encrypted += RotorContact.Instance().ContactToCharacter(machine.PressKey(char))

print("Encrypted : {0}".format(encrypted))
