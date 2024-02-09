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
#ifndef ENIGMAMACHINETYPES_H
#define ENIGMAMACHINETYPES_H
#include <map>
#include <string>
#include "EnigmaMachineType.h"
#include "RotorFactory.h"
#include "EnigmaMachineDefinition.h"

namespace enigmaSimulator {

    const std::map<EnigmaMachineDefinition, EnigmaMachineType> ENIGMA_MODELS = {

        // The Enigma I was the main Enigma machine used by the German Army and
        // Air Force. The military machines were the only ones with a plug board. The
        // ETW and all three known UKWs. UKW-A was used before WWII. UKW-B was the
        // standard reflector during the war and UKW-C was only used in the later
        // part of the war. The wiring of the five wheels is identical to the
        // wiring of the first 5 wheels of the Enigma M3 (Navy) and the U-Boot
        // Enigma M4.
        { kEnigmaMachineDefinition_Enigma1,
          EnigmaMachineType (
            "Enigma Model 1",
            "Enigma1",
            enigmaSimulator::kRotorCount_3,
            true,
            enigmaSimulator::RotorNamesList { ENIGMA_1_ROTOR_I,
                                              ENIGMA_1_ROTOR_II,
                                              ENIGMA_1_ROTOR_III,
                                              ENIGMA_1_ROTOR_IV,
                                              ENIGMA_1_ROTOR_V },
            enigmaSimulator::ReflectorNamesList { }
          )
        },

        // The Enigma M1, M2 and M3 machines were used by the German Navy
        // (Kriegsmarine). They are basically compatible with the Enigma I. The
        // wiring of the Enigma M3 is given in the table below. Wheels I thru V
        // are identical to those of the Enigma I. The same is true for UKW B
        // and C. The three additional wheels (VI, VII and VIII) were used
        // exclusively by the Kriegsmarine. The machine is also compatible with
        // the Enigma M4 (when the 4th wheel of the M4 is set to position 'A').
        { kEnigmaMachineDefinition_EnigmaModelM3,
          EnigmaMachineType (
            "Enigma Model M3",
            "M3",
            enigmaSimulator::kRotorCount_3,
            true,
            enigmaSimulator::RotorNamesList { ENIGMA_M3_ROTOR_I,
                                              ENIGMA_M3_ROTOR_II,
                                              ENIGMA_M3_ROTOR_III,
                                              ENIGMA_M3_ROTOR_IV,
                                              ENIGMA_M3_ROTOR_V,
                                              ENIGMA_M3_ROTOR_VI,
                                              ENIGMA_M3_ROTOR_VII,
                                              ENIGMA_M3_ROTOR_VIII,
                                              },
            enigmaSimulator::ReflectorNamesList { }
          )
        },

        // The Enigma M4 was a further development of the M3 and was used
        // exclusively by the German Navy U-boat division (Kriegsmarine). It
        // was introduced unexpectedly on 2 February 1942. UKW-B was the
        // standard reflector throughout the war and UKW-C was only temporarily
        // used during the war. The wiring of the first 5 wheels (I-V) are
        // identical to the wiring of the 5 wheels of the Enigma I, that was
        // used by the Wehrmacht and Luftwaffe. This allowed secure
        // communication between the departments.
        // Bletchley Park called the messages to and from Atlantic U-boats by
        // the code name "Shark", the rest of the traffic they called "Dolphin.
        { kEnigmaMachineDefinition_EnigmaModelM4,
          EnigmaMachineType (
            "German Navy 4-rotor M4 Enigma",
            "M4",
            enigmaSimulator::kRotorCount_4,
            true,
            enigmaSimulator::RotorNamesList { ENIGMA_M4_ROTOR_I,
                                              ENIGMA_M4_ROTOR_II,
                                              ENIGMA_M4_ROTOR_III,
                                              ENIGMA_M4_ROTOR_IV,
                                              ENIGMA_M4_ROTOR_V,
                                              ENIGMA_M4_ROTOR_VI,
                                              ENIGMA_M4_ROTOR_VII,
                                              ENIGMA_M4_ROTOR_VIII,
                                              },
            enigmaSimulator::ReflectorNamesList { }
          )
        }
    };

}   // namespace enigmaSimulator

#endif  //  ENIGMAMACHINETYPES_H
