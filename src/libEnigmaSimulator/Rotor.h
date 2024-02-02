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
#include <string>
#include <vector>
#include "RotorContact.h"

namespace enigmaSimualator {

    const int MAX_CONTACT_NO = 25;
    const int WIRING_LENGTH = 26;

    // Class representing an Enigma rotor wheel / drum / Walzen.
    class Rotor
    {
    public:
        Rotor (
            std::string rotor_name,
            std::string wiring_name,
            std::vector<RotorContact> notch_locations);

        // Property getter : Name of the rotor.
        inline std::string RotorName () { return rotor_name_; }

        // Property getter : Name of the wiring setup.
        inline std::string WiringName () { return wiring_name_; }

        inline std::vector<RotorContact> Notches () { return notch_locations_; }

        // Property getter : Position of the rotor.
        inline RotorContact RotorPosition () { return rotor_position_; }

        void RotorPosition (RotorContact position);

        void Step ();

        void Encrypt (RotorContact contact, bool forward = true);

        bool WillStepNext ();

        int DetermineNextPosition (int contact);

    protected:
        std::string rotor_name_;
        std::string wiring_name_;
        std::vector<RotorContact> notch_locations_;
        RotorContact rotor_position_;
    };

}   // namespace enigmaSimualator

#endif  //  #ifndef ROTOR_H
