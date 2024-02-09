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
#include <map>
#include "ReflectorFactory.h"

namespace enigmaSimulator {

std::map<std::string, std::string> REFLECTORS =
{
    // Enigma I
    { ENIGMA_1_REFLECTOR_UKW_A, "EJMZALYXVBWFCRQUONTSPIKHGD" },
    { ENIGMA_1_REFLECTOR_UKW_B, "YRUHQSLDPXNGOKMIEBFZCWVJAT" },
    { ENIGMA_1_REFLECTOR_UKW_C, "FVPJIAOYEDRZXWGCTKUQSBNMHL" },

    // Enigma Model M3
    { ENIGMA_M3_REFLECTOR_UKW_B, "YRUHQSLDPXNGOKMIEBFZCWVJAT" },
    { ENIGMA_M3_REFLECTOR_UKW_C, "FVPJIAOYEDRZXWGCTKUQSBNMHL" },

    // German Navy 4-rotor M4 Enigma
    { ENIGMA_M4_REFLECTOR_UKW_B, "ENKQAUYWJICOPBLMDXZVFTHRGS" },
    { ENIGMA_M4_REFLECTOR_UKW_C, "RDOBJNTKVEHMLFCWZAXGYIPSUQ" }
};

}   // namespace enigmaSimulator
