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
#include "EnigmaMachineTypes.h"

namespace enigmaSimulator {

    // Implementation of the Enigma machine machine.
    class EnigmaMachine
    {
    protected:
        bool is_configured_;
        std::string last_error_;
        Plugboard *plugboard_;
        IReflector *reflector_;

    public:
#ifdef __PY__
        __slots__ = ['_double_step', '_is_configured', '_last_error', '_logger',
                     '_model_details', '_plugboard', '_reflector', '_rotors']
#endif

        EnigmaMachine();

        inline bool IsConfigured() { return is_configured_; }

        // Get the last reported error in human-readable form.
        inline std::string LastError() { return last_error_; }

        // Get the plugboard, it can be a nullptr if a plugboard hasn't been
        // configured.
        Plugboard *plugboard() { return plugboard_; }

        // Get the reflector.
        IReflector *reflector() { return reflector_; }

        bool Configure(EnigmaMachineDefinition model,
                       RotorNamesList rotors,
                       ReflectorNamesList reflector);

        RotorContact PressKey(RotorContact key);

        void SetRotorPosition(int rotor_no, RotorContact position);

        void GetRotorPosition(int rotorNo);

    protected:

        void StepRotors( ):

        void _log_rotor_states(self, prefix_str : str);
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ENIGMAMACHINE_H

// # 253 #