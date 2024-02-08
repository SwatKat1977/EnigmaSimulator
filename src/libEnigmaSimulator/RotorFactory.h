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
#ifndef ROTORFACTORY_H
#define ROTORFACTORY_H
#include <string>
#include "Rotor.h"

namespace enigmaSimulator {

    //  Enigma Model M1 Rotors
    const std::string ENIGMA_1_I = "Enigma1_I";
    const std::string ENIGMA_1_II = "Enigma1_II";
    const std::string ENIGMA_1_III = "Enigma1_III";
    const std::string ENIGMA_1_IV = "Enigma1_IV";
    const std::string ENIGMA_1_V = "Enigma1_V";

    // Enigma Model M3
    const std::string ENIGMA_M3_I = "EnigmaM3_I";
    const std::string ENIGMA_M3_II = "EnigmaM3_II";
    const std::string ENIGMA_M3_III = "EnigmaM3_III";
    const std::string ENIGMA_M3_IV = "EnigmaM3_IV";
    const std::string ENIGMA_M3_V = "EnigmaM3_V";
    const std::string ENIGMA_M3_VI = "EnigmaM3_VI";
    const std::string ENIGMA_M3_VII = "EnigmaM3_VII";
    const std::string ENIGMA_M3_VIII = "EnigmaM3_VIII";

    // German Navy 4-rotor M4 Enigma
    const std::string ENIGMA_M4_I = "EnigmaM4_I";
    const std::string ENIGMA_M4_II = "EnigmaM4_II";
    const std::string ENIGMA_M4_III = "EnigmaM4_III";
    const std::string ENIGMA_M4_IV = "EnigmaM4_IV";
    const std::string ENIGMA_M4_V = "EnigmaM4_V";
    const std::string ENIGMA_M4_VI = "EnigmaM4_VI";
    const std::string ENIGMA_M4_VII = "EnigmaM4_VII";
    const std::string ENIGMA_M4_VIII = "EnigmaM4_VIII";

    Rotor *CreateRotor(std::string rotorName);

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTORFACTORY_H
