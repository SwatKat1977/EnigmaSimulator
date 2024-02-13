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
#ifndef ROTOR_H
#define ROTOR_H
#include <vector>
#include "IRotor.h"

namespace enigmaSimulator {

    // Class representing an Enigma rotor wheel / drum / Walzen.
    class Rotor : public IRotor
    {
    public:
        Rotor (
            std::string rotor_name,
            RotorWiringLayout wiring_,
            std::vector<RotorContact> notches,
            RotorContact initialPosition = kRotorContact_A);

        ~Rotor () = default;

        // Property getter : Name of the rotor.
        inline std::string RotorName () { return rotor_name_; }

        // Property getter : Wiring setup.
        inline RotorWiringLayout Wiring () { return wiring_; }

        inline std::vector<RotorContact> Notches () { return notches_; }

        // Property getter : Position of the rotor.
        inline RotorContact RotorPosition () { return rotor_position_; }

        void RotorPosition (RotorContact position);

        void Step ();

        RotorContact Encrypt (RotorContact contact, bool forward = true);

        bool WillStepNext ();

        RotorContact OffsetContactPosition (RotorContact contact, const int offset);

        void PrettyPrintWiring();

    protected:
        std::string rotor_name_;
        RotorWiringLayout wiring_;
        std::vector<RotorContact> notches_;
        RotorContact rotor_position_;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTOR_H
