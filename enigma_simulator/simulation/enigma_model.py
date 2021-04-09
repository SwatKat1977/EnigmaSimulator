'''
    EnigmaSimulator - A software implementation of the Engima Machine.
    Copyright (C) 2015-2021 Engima Simulator Development Team

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

class RotorCount(Enum):
    ''' Enumeration for total number of rotors. '''

    THREE = 3
    FOUR = 4

class EnigmaModel:
    ''' Definition of an Enigma model. '''
    __slots__ = ['_has_plugboard', '_long_name', '_rotors', '_reflectors',
                 '_short_name', '_total_rotors']
    # pylint: disable=too-many-arguments

    @property
    def long_name(self) -> str:
        ''' Get name of model for the Enigma machine. '''
        return self._long_name

    @property
    def short_name(self) -> str:
        ''' Get name of model for the Enigma machine. '''
        return self._short_name

    @property
    def no_of_rotors(self) -> RotorCount:
        ''' Get the total number of rotors for Enigma machine. '''
        return self._total_rotors

    @property
    def has_plugboard(self) -> bool:
        ''' Get the Enigma machine has a plugboard flag. '''
        return self._has_plugboard

    @property
    def rotors(self) -> bool:
        ''' Get the list of available rotors for the machine. '''
        return self._rotors

    @property
    def reflectors(self) -> bool:
        ''' Get the list of available reflectors for the machine. '''
        return self._reflectors

    def __init__(self, long_name : str, short_name : str,
                 total_rotor : RotorCount, has_plugboard : bool,
                 rotors : list, reflectors : list):

        if not isinstance(total_rotor, (RotorCount)):
            raise ValueError("Invalid number of rotors")

        self._has_plugboard = has_plugboard
        self._long_name = long_name
        self._rotors = rotors
        self._reflectors = reflectors
        self._short_name = short_name
        self._total_rotors = total_rotor
