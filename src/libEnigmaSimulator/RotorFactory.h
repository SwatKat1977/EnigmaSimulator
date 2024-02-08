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
#ifndef ROTORFACTORY_H
#define ROTORFACTORY_H
#include <string>
#include "Rotor.h"

namespace enigmaSimulator {

    Rotor *CreateRotor(std::string rotorName);

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTORFACTORY_H
