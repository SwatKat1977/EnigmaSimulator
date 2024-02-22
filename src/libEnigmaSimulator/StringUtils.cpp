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
#include "Definitions.h"
#include "RotorContact.h"
#include "StringUtils.h"

namespace enigmaSimulator {

    // In-place string left rotatation by 'offset' positions.
    void LeftRotateString (std::string& str, int offset)
    {
        std::reverse (str.begin (), str.begin () + offset);
        std::reverse (str.begin () + offset, str.end ());
        std::reverse (str.begin (), str.end ());
    }

    // In-place string right rotatation by 'offset' positions.
    void RightRotateString (std::string& str, int offset)
    {
        LeftRotateString (str, static_cast<int>(str.length ()) - offset);
    }

    // Offset each letter by 'offset' amount, so if offset = 1 then 'A' becomes
    // 'B'.
    void OffsetStringValue (std::string& str, int offset)
    {
        for (int idx = 0; idx < str.size(); idx++)
        {
            int newLetter = ((str[idx] - 65) + 1) + offset;
            newLetter = (newLetter > kRotorContact_Z) ?
                (newLetter % MAX_WIRING_ENTRIES) : newLetter;
            str[idx] = RotorContactStr[newLetter];
        }
    }

}   // namespace enigmaSimulator
