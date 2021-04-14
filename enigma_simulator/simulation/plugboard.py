'''
    <one line to give the program's name and a brief idea of what it does.>
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
from simulation.rotor_contact import RotorContact

class Plugboard:
    ''' Class representing an Enigma plugboard / Steckerbrett (German). '''
    __slots__ = ['_wiring']

    def __init__(self):
        self._wiring = {}

        for letter in RotorContact:
            self._wiring[letter] = letter

    def set_plug(self, src : RotorContact, dest : RotorContact) -> None:
        '''
        Set a plug, given a source and destination. Only 1 plug is allowed per
        hole. If this, occurs then a ValueError exception is raised. If the src
        or dest are not RotorContacts a ValueError is also raised.
        @param src Source of the plug.
        @param dest Destination of the plug.
        '''
        if not isinstance(src, (RotorContact)):
            raise ValueError("Source plug position not valid")

        if not isinstance(dest, (RotorContact)):
            raise ValueError("Destination plug position not valid")

        if self._wiring[src] != src:
            raise ValueError(f'Plugboard source ({src.name}:{dest.name}) ' + \
                'is already used')

        if self._wiring[dest] != dest:
            raise ValueError(f'Plugboard destination ({src.name}:' + \
                '{dest.name}) is already in use')

        self._wiring[src] = dest
        self._wiring[dest] = src

    def get_plug(self, src : RotorContact) -> RotorContact:
        '''
        Get the opposite end of a plug. If there is a plug then work out the
        other end, otherwise return same letter to represent no plug.
        @param src Plug to get the other end of.
        @return Other end of plug.  For example if 'A' is wired to 'T' then 'T'
        would be returned, but if 'C' wasn't wired then 'C' is returned.
        '''
        if not isinstance(src, (RotorContact)):
            raise ValueError("Invalid plug position")

        # Check that the plug is fitted, if it has then modify the outgoing
        # value, otherwisevuse pass-though (same letter in is returned).
        return self._wiring[src] if self._wiring[src] != src else src
