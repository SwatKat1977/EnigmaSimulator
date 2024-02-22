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
#include "gtest/gtest.h"
#include "Reflector.h"
#include "ReflectorTest.h"

TEST_F(ReflectorTest, ConstructWithValidWiring)
{
    /*
    Test construction of reflector with an valid wiring layout, it should
    result in the construction of a reflector object.
    */
    try
    {
        auto rotor = enigmaSimulator::Reflector(
            "Valid Reflector", valid_wiring_layout_);
    }
    catch(const std::exception&)
    {
        FAIL() << "Expected valid reflector wiring";
    }
}

TEST_F(ReflectorTest, ConstructWithInvalidWiring)
{
    /*
    Test construction of reflector with an invalid wiring layout, it should
    result in a std::runtime_error being thrown with the description text of
    'Wiring layout is not valid'.
    */
    try
    {
        auto rotor = enigmaSimulator::Reflector(
            "Invalid Reflector", invalid_wiring_layout_);
        FAIL() << "Expected invalid reflector wiring";
    }
    catch(const std::exception&)
    {
    }
}
