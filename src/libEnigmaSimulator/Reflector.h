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
#ifndef REFLECTOR_H
#define REFLECTOR_H
#include <map>
#include <string>
#include "IReflector.h"
#include "RotorContact.h"
#include "RotorWireConfiguration.h"

namespace enigmaSimulator {

    // Implementation of an Enigma reflector.
    class Reflector : public IReflector
    {
    public:

        Reflector(std::string name, RotorWireConfiguration wiring);

        ~Reflector() = default;

        inline const std::string Name() { return name_; }

        inline const RotorWireConfiguration Wiring() { return wiring_; }

        RotorContact Encrypt(RotorContact contact, bool forward = true);

    protected:
        std::string name_;
        RotorWireConfiguration wiring_;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef REFLECTOR_H
