/*
    Engima Machine Simulator
    Copyright (C) 2015-2024 Engima Simulator Development Team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
*/
from simulation.rotor_contact import RotorContact

namespace enigmaSimulator {

class Reflector:
    ''' Implementation of an Enigma reflector. '''
    __slots__ = ['_name', '_wiring']

    # The number of pins or contacts on a reflector.
    NumberOfReflectorPins = 26

    @property
    def name(self):
        ''' Property getter : Human readable name of the reflector. '''
        return self._name

    @property
    def wiring(self):
        ''' Property getter : How the reflector is wired. '''
        return self._wiring

    def __init__(self, name, wiring):
        '''
        Reflector constructor.
        @param name The human readable reflector name.
        @param wiring Wiring setting from right to left.
        '''
        self._name = name

        # Check to make sure wiring is a list.
        if not isinstance(wiring, str):
            raise ValueError("Reflector wiring should be a string")

        if len(wiring) != self.NumberOfReflectorPins:
            raise ValueError("Reflector wiring string incorrect")

        # define how the rotor is internally wired.
        self._wiring = wiring

    def encrypt(self, contact : RotorContact) -> RotorContact:
        '''
        Using the reflector, encrpyt the contact using the pins on the
        right-hand side of the reflector.
        #  @param contact Input contact to encrypt.
        #  @return If successful a contact number is returned, on error a
        #  ValueError exception is raised.
        '''
        return RotorContact[self._wiring[contact.value]]

}   // namespace enigmaSimulator
