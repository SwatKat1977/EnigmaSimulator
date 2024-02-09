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
#ifndef ENIGMAMACHINE_H
#define ENIGMAMACHINE_H
#include <string>
#include "IReflector.h"
#include "Plugboard.h"
#include "EnigmaMachineDefinition.h"
#include "EnigmaMachineType.h"
#include "Rotor.h"

namespace enigmaSimulator {

    enum RotorPositionNumber
    {
        kRotorPositionNumber_1 = 0,
        kRotorPositionNumber_2 = 1,
        kRotorPositionNumber_3 = 2,
        kRotorPositionNumber_4 = 3
    };

    // Implementation of the Enigma machine machine.
    class EnigmaMachine
    {
    public:

#ifdef __PY__
        __slots__ = ['_double_step'
#endif

        EnigmaMachine();

        inline bool IsConfigured() { return is_configured_; }

        // Get the last reported error in human-readable form.
        inline std::string LastError() { return lastError_; }

        // Get the plugboard, it can be a nullptr if a plugboard hasn't been
        // configured.
        Plugboard *plugboard() { return plugboard_; }

        // Get the reflector.
        IReflector *reflector() { return reflector_; }

        bool Configure(EnigmaMachineDefinition machineType,
                       RotorNamesList rotors,
                       std::string reflectorName);

        RotorContact PressKey(RotorContact key);

        void SetRotorPosition(int rotor_no, RotorContact position);

        void GetRotorPosition(int rotorNo);

    protected:
        bool is_configured_;
        std::string lastError_;
        Plugboard *plugboard_;
        IReflector *reflector_;
        EnigmaMachineDefinition type_;
        std::map<RotorPositionNumber, std::unique_ptr<Rotor>> rotors_;

        void StepRotors( );

        void LogRotorStates(std::string prefix_str);
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ENIGMAMACHINE_H
