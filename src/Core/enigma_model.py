'''
    EnigmaSimulator - A software implementation of the Engima Machine.
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
    __slots__ = ['_has_plugboard', '_long_name', '_short_name', '_total_rotors']

    ## Get name of model for the Enigma machine.
    #  @param self The object pointer.
    @property
    def long_name(self):
        return self._long_name

    ## Get name of model for the Enigma machine.
    #  @param self The object pointer.
    @property
    def short_name(self):
        return self._short_name

    ## Get the total number of rotors for Enigma machine.
    #  @param self The object pointer.
    @property
    def no_of_rotors(self):
        return self._total_rotors

    ## Get flag to say if the Enigma machine has a plugboard.
    #  @param model Enigma machine mode.
    @property
    def has_plugboard(self):
        return self._has_plugboard


    ## Constructor, create a machine setup.
    #  @param model Enigma machine mode.
    #  @param selectedRotors The name of rotors used by the Enigma machine.
    #  @param plugboard Enigma plugboard (None if machine doesn't use one).
    def __init__(self, long_name, short_name, total_rotor, has_plugboard):

        # Check to make sure total_rotors is enumeration from  is a PlugBoard or None.
        if not isinstance(total_rotor, (RotorCount)):
            raise ValueError("Invalid number of rotors")

        self._has_plugboard = has_plugboard
        self._long_name = long_name
        self._short_name = short_name
        self._total_rotors = total_rotor
