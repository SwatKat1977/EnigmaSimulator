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
from enum import Enum


## Enumeration for total number of rotors.
class RotorCount(Enum):
    ThreeRotors = 3
    FourRotors = 4


## Implementation of Enigma model setup.
class EnigmaModel:
    __slots__ = ['has_plugboard', 'model_name', 'total_rotors']

    ## Get name of model for the Enigma machine.
    #  @param self The object pointer.
    @property
    def name(self):
        return self.model_name

    ## Get the total number of rotors for Enigma machine.
    #  @param self The object pointer.
    @property
    def no_of_rotors(self):
        return self.total_rotors

    ## Get flag to say if the Enigma machine has a plugboard.
    #  @param model Enigma machine mode.
    @property
    def plugboard(self):
        return self.has_plugboard


    ## Constructor, create a machine setup.
    #  @param model Enigma machine mode.
    #  @param selectedRotors The name of rotors used by the Enigma machine.
    #  @param plugboard Enigma plugboard (None if machine doesn't use one).
    def __init__(self, model_nwme, total_rotor, has_plugboard):

        # Check to make sure total_rotors is enumeration from  is a PlugBoard or None.
        if not isinstance(total_rotor, (RotorCount)):
            raise ValueError("Invalid number of rotors")

        self.model_name = model_nwme
        self.total_rotors = total_rotor
        self.has_plugboard = has_plugboard
