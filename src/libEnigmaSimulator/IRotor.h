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
#ifndef VERSION_H
#define VERSION_H
#include <string>
#include "RotorContact.h"
#include "RotorWiringLayout.h"

namespace enigmaSimulator {

    class IRotor
    {
    public:
        // Property getter : Name of the rotor.
        virtual std::string RotorName () = 0;

        // Property getter : Wiring setup.
        virtual RotorWiringLayout Wiring () = 0;

        // Property getter : Turnover notches.
        virtual std::vector<RotorContact> Notches () = 0;

        // Property getter : Position of the rotor.
        virtual RotorContact RotorPosition () = 0;

#ifdef BROKEN
        virtual void RotorPosition (RotorContact position) = 0;
#endif  //  #ifdef BROKEN

        virtual void Step () = 0;

#ifdef BROKEN
        virtual RotorContact Encrypt (
            RotorContact contact,
            bool forward = true) = 0;
#endif  //  #ifdef BROKEN

        virtual bool WillStepNext () = 0;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef VERSION_H
