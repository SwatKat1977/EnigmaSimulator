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
#ifndef PLUGBOARDEST_H
#define PLUGBOARDEST_H
#include "Common.h"
#include "Plugboard.h"

class PlugboardTest : public testing::Test {
 protected:
    enigmaSimulator::Plugboard plugboard_;

    void SetUp() override
    {
    }

    void TearDown() override
    {
    }
};

#endif  //  #ifndef PLUGBOARDEST_H
