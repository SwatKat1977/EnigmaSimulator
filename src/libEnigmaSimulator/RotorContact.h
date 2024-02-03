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
#ifndef ROTORCONTACT_H
#define ROTORCONTACT_H

namespace enigmaSimualator {

    // Enumeration of a rotor contact character (A-Z)
    enum RotorContact
    {
        kRotorContact_A = 0,
        kRotorContact_B = 1,
        kRotorContact_C = 2,
        kRotorContact_D = 3,
        kRotorContact_E = 4,
        kRotorContact_F = 5,
        kRotorContact_G = 6,
        kRotorContact_H = 7,
        kRotorContact_I = 8,
        kRotorContact_J = 9,
        kRotorContact_K = 10,
        kRotorContact_L = 11,
        kRotorContact_M = 12,
        kRotorContact_N = 13,
        kRotorContact_O = 14,
        kRotorContact_P = 15,
        kRotorContact_Q = 16,
        kRotorContact_R = 17,
        kRotorContact_S = 18,
        kRotorContact_T = 19,
        kRotorContact_U = 20,
        kRotorContact_V = 21,
        kRotorContact_W = 22,
        kRotorContact_X = 23,
        kRotorContact_Y = 24,
        kRotorContact_Z = 25,
        kRotorContact_end
    };

    static const char *RotorContactStr[] =
    {
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    };

}   // namespace enigmaSimualator

#endif  //  #ifndef ROTORCONTACT_H
