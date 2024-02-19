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
#ifndef IWIREDROTARYDEVICE_H
#define IWIREDROTARYDEVICE_H
#include "RotorContact.h"

namespace enigmaSimulator {

    class IWiredRotaryDevice
    {
    public:

        ~IWiredRotaryDevice () { }

    protected:
        virtual bool HasValidWiring () = 0;

        virtual RotorContact GetDestination (const RotorContact src,
            bool forward = true) = 0;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef IWIREDROTARYDEVICE_H
