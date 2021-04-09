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

class MachineType:
    __slots__ = ['_has_plugboard', '_name', '_short_name']

    def __init__(self, name : str, short_name : str,  has_plugboard : bool,
                 rotors : list, reflectors : list) -> None:

        self._has_plugboard = has_plugboard
        self._name = name
        self._reflectors = reflectors
        self._rotors = rotors
        self._short_name = short_name
