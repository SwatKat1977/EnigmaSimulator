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
#ifndef IWIRECONFIGUREDDEVICE_H
#define IWIRECONFIGUREDDEVICE_H
#include "RotorContact.h"

namespace enigmaSimulator {

    struct WiringEntry
    {
        RotorContact src;
        RotorContact dest;
    };

    class IWireConfiguredDevice
    {
    public:

        ~IWireConfiguredDevice () { }

        virtual bool HasValidWiring () = 0;

        virtual RotorContact WiringPathForward (const RotorContact src) = 0;
        virtual RotorContact WiringPathReverse (const RotorContact dest) = 0;
#ifdef __TO_BE_IMPLEMENTED__
        virtual void FirstWiringPath () = 0;
        virtual void NextWiringPath () = 0;
        virtual WiringEntry CurrentWiringPath () = 0;
#endif
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef IWIRECONFIGUREDDEVICE_H
