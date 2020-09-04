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


## Enigma machine G was modified to the Enigma I by June 1930.  Enigma I is
#  also known as the Wehrmacht, or "Services" Enigma, and was used extensively
#  by German military services and other government organisations (such as the
#  railways) before and during World War II.
ENIGMA_MODEL_1 = EnigmaModel('Enigma Model 1', 'Enigma1', RotorCount.ThreeRotors, True)

## Enigma A, also known as Die kleine Militärmaschine (the small military
#  machine), was an electro­mechanical rotor-based cipher machine, introduced
#  in 1924 by Chiffriermaschinen Aktien­gesell­schaft (ChiMaAG) in Berlin
#  (Germany). It was the first Enigma that used light bulbs for its output.
ENIGMA_MODEL_AORB = EnigmaModel('Enigma Model A or B', 'ModelAorB', RotorCount.ThreeRotors, True)

## The M2 and M2a variants were followed in 1939/1940 by the M3, which was the
#  last series of 3-wheel naval Enigma machines. Like with the other versions,
#  the exact differences between the M3 and the earlier ones are not known.
ENIGMA_MODEL_M3 = EnigmaModel('Enigma Model M3', 'M3', RotorCount.ThreeRotors, True)

## On 1 February 1942, the Enigma messages to and from Atlantic U-boats, which
#  Bletchley Park called '"Shark," became significantly different from the rest
#  of the traffic, which they called "Dolphin.
ENIGMA_MODEL_M4 = EnigmaModel('German Navy 4-rotor M4 Enigma', 'M4',
                              RotorCount.FourRotors, True)
