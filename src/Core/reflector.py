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


# ***********************************************************************
# Implementation of class representing an Enigma reflector.
# ***********************************************************************
class Reflector:
    __slots__ = ['reflector_name', 'reflector_wiring']

    # The number of pins or contacts on a reflector.
    NumberOfReflectorPins = 26

    ## Property getter : Human readable name of the reflector.
    @property
    def name(self):
        return self.reflector_name

    ## Property getter : How the reflector is wired.
    @property
    def wiring(self):
        return self.reflector_wiring


    ## Constructor.. Wiring is from right => left
    #  @param name The human readable reflector name.
    #  @param wiring Wiring setting from right to left.
    def __init__(self, name, wiring):
        self.reflector_name = name

        # Check to make sure wiring is a list.
        if not isinstance(wiring, (dict)):
            raise ValueError("Incompatible reflector wiring diagram")

        if len(wiring) != self.NumberOfReflectorPins:
            raise ValueError("Incomplete reflector wiring diagram")

        # define how the rotor is internally wired.
        self.reflector_wiring = wiring


    ## Get the output (circuit) using pins on the right-hand side of the
    #  reflector.
    #  @param pin_no Reference pin to get circuit with.
    #  @return If successful a contact number is returned, on error a
    #  ValueError exception is raised.
    def get_circuit(self, pin):
        return self.reflector_wiring[pin.value]
