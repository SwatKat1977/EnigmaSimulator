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
#ifndef REFLECTORTEST_H
#define REFLECTORTEST_H
#include "Common.h"
#include "RotorWiringLayout.h"

class ReflectorTest : public testing::Test {
 protected:
    enigmaSimulator::RotorWiringLayout valid_wiring_layout_;
    enigmaSimulator::RotorWiringLayout invalid_wiring_layout_;

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
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_A,
                                       enigmaSimulator::kRotorContact_E);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_B,
                                       enigmaSimulator::kRotorContact_K);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_C,
                                       enigmaSimulator::kRotorContact_M);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_D,
                                       enigmaSimulator::kRotorContact_F);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_E,
                                       enigmaSimulator::kRotorContact_L);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_F,
                                       enigmaSimulator::kRotorContact_G);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_G,
                                       enigmaSimulator::kRotorContact_D);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_H,
                                       enigmaSimulator::kRotorContact_Q);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_I,
                                       enigmaSimulator::kRotorContact_V);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_J,
                                       enigmaSimulator::kRotorContact_Z);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_K,
                                       enigmaSimulator::kRotorContact_N);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_L,
                                       enigmaSimulator::kRotorContact_T);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_M,
                                       enigmaSimulator::kRotorContact_O);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_N,
                                       enigmaSimulator::kRotorContact_W);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_O,
                                       enigmaSimulator::kRotorContact_Y);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_P,
                                       enigmaSimulator::kRotorContact_H);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_Q,
                                       enigmaSimulator::kRotorContact_X);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_R,
                                       enigmaSimulator::kRotorContact_U);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_S,
                                       enigmaSimulator::kRotorContact_S);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_T,
                                       enigmaSimulator::kRotorContact_P);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_U,
                                       enigmaSimulator::kRotorContact_A);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_V,
                                       enigmaSimulator::kRotorContact_I);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_W,
                                       enigmaSimulator::kRotorContact_B);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_X,
                                       enigmaSimulator::kRotorContact_R);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_Y,
                                       enigmaSimulator::kRotorContact_C);
        valid_wiring_layout_.AddEntry (enigmaSimulator::kRotorContact_Z,
                                       enigmaSimulator::kRotorContact_J);
    }
};

#endif  //  #ifndef REFLECTORTEST_H
