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
#include <string>
#include "RotorFactory.h"
#include "RotorWiringLayout.h"

namespace enigmaSimulator {

struct RotorEntry
{
    std::string layout;
    std::string notches;
};

using RotorsMap = std::map<std::string, RotorEntry>;

RotorsMap ROTORS =
{
    // Enigma I
    { ENIGMA_1_ROTOR_I,   { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Y" } },
    { ENIGMA_1_ROTOR_II,  { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "M" } },
    { ENIGMA_1_ROTOR_III, { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "D" } },
    { ENIGMA_1_ROTOR_IV,  { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "R" } },
    { ENIGMA_1_ROTOR_V,   { "VZBRGITYUPSDNHLXAWMJQOFECK", "H" } },

    // Enigma Model M3
    { ENIGMA_M3_ROTOR_I,    { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q" } },
    { ENIGMA_M3_ROTOR_II,   { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E" } },
    { ENIGMA_M3_ROTOR_III,  { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V" } },
    { ENIGMA_M3_ROTOR_IV,   { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J" } },
    { ENIGMA_M3_ROTOR_V,    { "VZBRGITYUPSDNHLXAWMJQOFECK", "Z" } },
    { ENIGMA_M3_ROTOR_VI,   { "JPGVOUMFYQBENHZRDKASXLICTW", "ZM" } },
    { ENIGMA_M3_ROTOR_VII,  { "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM" } },
    { ENIGMA_M3_ROTOR_VIII, { "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM" } },

    // German Navy 4-rotor M4 Enigma
    { ENIGMA_M4_ROTOR_I,    { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q" } },
    { ENIGMA_M4_ROTOR_II,   { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E" } },
    { ENIGMA_M4_ROTOR_III,  { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V" } },
    { ENIGMA_M4_ROTOR_IV,   { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J" } },
    { ENIGMA_M4_ROTOR_V,    { "VZBRGITYUPSDNHLXAWMJQOFECK", "Z" } },
    { ENIGMA_M4_ROTOR_VI,   { "JPGVOUMFYQBENHZRDKASXLICTW", "ZM" } },
    { ENIGMA_M4_ROTOR_VII,  { "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM" } },
    { ENIGMA_M4_ROTOR_VIII, { "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM" } }
};

IRotor *CreateRotor(std::string rotorName)
{
    RotorsMap::iterator it = ROTORS.find(rotorName);

    if (it == ROTORS.end())
    {
        throw std::runtime_error("Invalid rotor '" + rotorName + "'");
    }

    RotorEntry entry = it->second;

    std::vector<RotorContact> notches;

    if (entry.notches.size())
    {
        for (int i = 0; i < entry.notches.size(); i++)
        {
            auto notch = RotorContact((entry.notches.c_str()[i] -65) +1);
            notches.push_back(notch);
        }
    }

    return new Rotor(
        rotorName,
        RotorWiringLayout(entry.layout),
        notches);
}

}   // namespace enigmaSimulator
