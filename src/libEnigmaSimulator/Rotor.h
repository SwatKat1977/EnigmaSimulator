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
#include "RotorWireConfiguration.h"

namespace enigmaSimulator {

    // Class representing an Enigma rotor wheel / drum / Walzen.
    class Rotor : public IRotor
    {
    public:
        Rotor (
            std::string rotor_name,
            RotorWireConfiguration wiring_,
            std::vector<RotorContact> notches,
            RotorContact initialPosition = kRotorContact_A);

        ~Rotor () = default;

        // Property getter : Name of the rotor.
        inline std::string RotorName () { return rotor_name_; }

        // Property getter : Wiring setup.
        inline RotorWireConfiguration Wiring () { return wiring_; }

        inline std::vector<RotorContact> Notches () { return notches_; }

        // Property getter : Position of the rotor.
        inline RotorContact RotorPosition () { return rotor_position_; }

        void RotorPosition (RotorContact position);

        // Property getter : Position of the ring.
        inline RotorContact RingPosition() { return ring_position_; }

        // Property setter : Position of the ring.
        void RingPosition (RotorContact pos);

        void Step ();

        RotorContact EncryptForward (RotorContact contact);

        RotorContact EncryptReverse (RotorContact contact);

        bool WillStepNext ();

        RotorContact OffsetContactPosition (RotorContact contact, const int offset);

        void PrettyPrintWiring();

    protected:
        std::string rotor_name_;
        RotorWireConfiguration wiring_;
        RotorWireConfiguration wiring_default_;
        std::vector<RotorContact> notches_;
        RotorContact ring_position_;
        RotorContact rotor_position_;

        void RecalculateWiring ();
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTOR_H
