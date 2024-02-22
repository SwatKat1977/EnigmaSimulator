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

namespace enigmaSimulator {

    // Enumeration of a rotor contact character (A-Z)
    enum RotorContact
    {
        kRotorContact_A = 1,
        kRotorContact_B = 2,
        kRotorContact_C = 3,
        kRotorContact_D = 4,
        kRotorContact_E = 5,
        kRotorContact_F = 6,
        kRotorContact_G = 7,
        kRotorContact_H = 8,
        kRotorContact_I = 9,
        kRotorContact_J = 10,
        kRotorContact_K = 11,
        kRotorContact_L = 12,
        kRotorContact_M = 13,
        kRotorContact_N = 14,
        kRotorContact_O = 15,
        kRotorContact_P = 16,
        kRotorContact_Q = 17,
        kRotorContact_R = 18,
        kRotorContact_S = 19,
        kRotorContact_T = 20,
        kRotorContact_U = 21,
        kRotorContact_V = 22,
        kRotorContact_W = 23,
        kRotorContact_X = 24,
        kRotorContact_Y = 25,
        kRotorContact_Z = 26,
        kRotorContact_end
    };

    static const char RotorContactStr[] =
    {
        '-',
        'A',
        'B',
        'C',
        'D',
        'E',
        'F',
        'G',
        'H',
        'I',
        'J',
        'K',
        'L',
        'M',
        'N',
        'O',
        'P',
        'Q',
        'R',
        'S',
        'T',
        'U',
        'V',
        'W',
        'X',
        'Y',
        'Z',
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTORCONTACT_H
