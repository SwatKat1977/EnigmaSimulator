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
from enigma_model import EnigmaModel, RotorCount


ENIGMA_MODEL_1 = EnigmaModel('Enigma Model 1', 'Enigma1', RotorCount.ThreeRotors, True)

ENIGMA_MODEL_AORB = EnigmaModel('Enigma Model A or B', 'ModelAorB', RotorCount.ThreeRotors, True)

ENIGMA_MODEL_M3 = EnigmaModel('Enigma Model M3', 'M3', RotorCount.ThreeRotors, True)

## On 1 February 1942, the Enigma messages to and from Atlantic U-boats, which
#  Bletchley Park called '"Shark," became significantly different from the rest
#  of the traffic, which they called "Dolphin.
ENIGMA_MODEL_M4 = EnigmaModel('German Navy 4-rotor M4 Enigma', 'M4',
                              RotorCount.FourRotors, True)
