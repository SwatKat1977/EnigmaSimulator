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
#ifndef REFLECTORFACTORY_H
#define REFLECTORFACTORY_H
#include <string>
#include "Reflector.h"

namespace enigmaSimulator {

    // Enigma Model 1
    const std::string ENIGMA_1_REFLECTOR_UKW_A = "Enigma1_Reflector_UKW-A";
    const std::string ENIGMA_1_REFLECTOR_UKW_B = "Enigma1_Reflector_UKW-B";
    const std::string ENIGMA_1_REFLECTOR_UKW_C = "Enigma1_Reflector_UKW-C";

    // Enigma Model M3
    const std::string ENIGMA_M3_REFLECTOR_UKW_B = "EnigmaM3_Reflector_UKW-B";
    const std::string ENIGMA_M3_REFLECTOR_UKW_C = "EnigmaM3_Reflector_UKW-C";

    // Enigma Model M4
    const std::string ENIGMA_M4_REFLECTOR_UKW_B = "EnigmaM4_Reflector_UKW-B";
    const std::string ENIGMA_M4_REFLECTOR_UKW_C = "EnigmaM4_Reflector_UKW-C";

    const Reflector CreateReflector (std::string reflectorName);

}   // namespace enigmaSimulator

#endif  //  #ifndef REFLECTORFACTORY_H
