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
#ifndef ROTORTEST_H
#define ROTORTEST_H
#include "Common.h"
#include "RotorWireConfiguration.h"

using namespace enigmaSimulator;

class RotorTest : public testing::Test {
 protected:
    enigmaSimulator::RotorWireConfiguration valid_wiring_layout_;
    enigmaSimulator::RotorWireConfiguration invalid_wiring_layout_;

    void SetUp() override
    {
        BuildValidWiringLayout();
    }

    void TearDown() override
    {
    }

private:
    void BuildValidWiringLayout()
    {
        std::string validLayout = "EKMFLGDQVZNTOWYHXUSPAIBRCJ";
        valid_wiring_layout_ = RotorWireConfiguration(validLayout);
    }
};

#endif  //  #ifndef ROTORTEST_H
