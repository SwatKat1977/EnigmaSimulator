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
#ifndef REFLECTORFACTORY_H
#define REFLECTORFACTORY_H
#include <string>
#include "Reflector.h"

namespace enigmaSimulator {

    const Reflector CreateReflector (std::string reflectorName);

}   // namespace enigmaSimulator

#endif  //  #ifndef REFLECTORFACTORY_H