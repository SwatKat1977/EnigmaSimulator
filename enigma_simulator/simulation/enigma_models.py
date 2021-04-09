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
from simulation.enigma_model import EnigmaModel, RotorCount, RotorDefintion

'''
Source for Engima machine types:
https://www.cryptomuseum.com/crypto/enigma/wiring.htm
'''

ENIGMA_MODELS = {
    # The Enigma I was the main Enigma machine used by the German Army and Air
    # Force. The military machines were the only ones with a plug board. The ETW
    # and all three known UKWs. UKW-A was used before WWII. UKW-B was the
    # standard reflector during the war and UKW-C was only used in the later part
    # of the war. The wiring of the five wheels is identical to the wiring of the
    # first 5 wheels of the Enigma M3 (Navy) and the U-Boot Enigma M4.
    'Enigma1' : EnigmaModel
    (
        'Enigma Model 1',
        'Enigma1',
        RotorCount.THREE,
        True,
        [
            RotorDefintion('I',   'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ['Q']),
            RotorDefintion('II',  'AJDKSIRUXBLHWTMCQGZNPYFVOE', ['E']),
            RotorDefintion('III', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ['V']),
            RotorDefintion('IV',  'ESOVPZJAYQUIRHXLNFTGKDCMWB', ['J']),
            RotorDefintion('V',   'VZBRGITYUPSDNHLXAWMJQOFECK', ['Z'])
        ],
        []
    ),

    # The Enigma M1, M2 and M3 machines were used by the German Navy
    # (Kriegsmarine). They are basically compatible with the Enigma I. The
    # wiring of the Enigma M3 is given in the table below. Wheels I thru V are
    # identical to those of the Enigma I. The same is true for UKW B and C. The
    # three additional wheels (VI, VII and VIII) were used exclusively by the
    # Kriegsmarine. The machine is also compatible with the Enigma M4 (when the
    # 4th wheel of the M4 is set to position 'A').
    'M3' : EnigmaModel
    (
        'Enigma Model M3',
        'M3',
        RotorCount.THREE,
        True,
        [
            RotorDefintion('I',    'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ['Q']),
            RotorDefintion('II',   'AJDKSIRUXBLHWTMCQGZNPYFVOE', ['E']),
            RotorDefintion('III',  'BDFHJLCPRTXVZNYEIWGAKMUSQO', ['V']),
            RotorDefintion('IV',   'ESOVPZJAYQUIRHXLNFTGKDCMWB', ['J']),
            RotorDefintion('V',    'VZBRGITYUPSDNHLXAWMJQOFECK', ['Z']),
            RotorDefintion('VI',   'JPGVOUMFYQBENHZRDKASXLICTW', ['Z', 'M']),
            RotorDefintion('VII',  'NZJHGRCXMYSWBOUFAIVLPEKQDT', ['Z', 'M']),
            RotorDefintion('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', ['Z', 'M'])
        ],
        []
    ),

    # The Enigma M4 was a further development of the M3 and was used
    # exclusively by the U-boat division of the German Navy (Kriegsmarine). It
    # was introduced unexpectedly on 2 February 1942. UKW-B was the standard
    # reflector throughout the war and UKW-C was only temporarily used during
    # the war. The wiring of the first 5 wheels (I-V)is identical to the wiring
    # of the 5 wheels of the Enigma I, that was used by the Wehrmacht and
    # Luftwaffe. This allowed secure communication between the departments.
    # Bletchley Park called the messages to and from Atlantic U-boats by the
    # code name "Shark", the rest of the traffic they called "Dolphin.
    'M4' : EnigmaModel
    (
        'German Navy 4-rotor M4 Enigma',
        'M4',
        RotorCount.FOUR,
        True,
        [
            RotorDefintion('I',    'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ['Q']),
            RotorDefintion('II',   'AJDKSIRUXBLHWTMCQGZNPYFVOE', ['E']),
            RotorDefintion('III',  'BDFHJLCPRTXVZNYEIWGAKMUSQO', ['V']),
            RotorDefintion('IV',   'ESOVPZJAYQUIRHXLNFTGKDCMWB', ['J']),
            RotorDefintion('V',    'VZBRGITYUPSDNHLXAWMJQOFECK', ['Z']),
            RotorDefintion('VI',   'JPGVOUMFYQBENHZRDKASXLICTW', ['Z', 'M']),
            RotorDefintion('VII',  'NZJHGRCXMYSWBOUFAIVLPEKQDT', ['Z', 'M']),
            RotorDefintion('VIII', 'FKQHTLXOCBJSPDZRAMEWNIUYGV', ['Z', 'M'])
        ],
        []
    )
}
