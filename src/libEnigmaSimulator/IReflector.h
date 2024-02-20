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
#ifndef IREFLECTOR_H
#define IREFLECTOR_H
#include <string>
#include "RotorContact.h"
#include "RotorWireConfiguration.h"

namespace enigmaSimulator {

    // Interface for Enigma reflector.
    class IReflector
    {
    public:

        virtual ~IReflector() {}

        virtual const std::string Name() = 0;

        virtual const RotorWireConfiguration Wiring() = 0;

        virtual RotorContact Encrypt(RotorContact contact, bool forward = true) = 0;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef IREFLECTOR_H
