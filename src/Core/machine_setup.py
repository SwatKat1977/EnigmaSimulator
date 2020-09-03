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
#from RotorsManager import rotorsManager


# ***********************************************************************
# Enumeration for number of rotors.
# *********************************************************************** 
class RotorCount(object):
    ThreeRotors = 3
    FourRotors = 4


# ***********************************************************************
# Enumeration for Enigma machine models.
# *********************************************************************** 
class EnigmaModel(object):
    ModelAorB = 'Model A or B'
    Enigma1 = 'Enigma 1'
    M3 = 'M3'
    M4 = 'M4'


# ***********************************************************************
# Implementation of machine setup.
# *********************************************************************** 
class MachineSetup(object):

    ##
    # Get model of the Enigma machine.
    # @return Model of the Enigma machine.
    @property
    def Model(self):
        return self._model

    ##
    # Get number of rotors for Enigma machine.
    # @return Number of rotors.
    @property
    def NumberOfRotors(self):
        return len(self._rotors)

    ##
    # Get rotors for Enigma machine.
    # @return list of rotors.
    @property
    def Rotors(self):
        return self._rotors

    ##
    # Get the machines plug board.
    # @return plugboard instance if using one, otherwise None.
    @property
    def Plugboard(self):
        return self._plugboard


    ##
    # Constructor, create a machine setup.
    # @param model Enigma machine mode.
    # @param selectedRotors The name of rotors used by the Enigma machine.
    # @param plugboard Enigma plugboard (None if machine doesn't use one).
    def __init__(self, model, selectedRotors, plugboard = None):
        self._model = model
        self._plugboard = plugboard
        self._rotors = selectedRotors
