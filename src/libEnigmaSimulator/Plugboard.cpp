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
#include <stdexcept>
#include "Plugboard.h"

namespace enigmaSimulator {

    Plugboard::Plugboard ()
    {
        Reset ();
    }

    /*
        Set a plug, given a source and destination. Only 1 plug is allowed per
        hole. If a second connection is attempted an exception is raised. If
        the source or destination are the same then an exception is also
        raised.
    */
    void Plugboard::SetPlug (RotorContact src, RotorContact dest)
    {

        if ((src == kRotorContact_end) ||
            (dest == kRotorContact_end))
        {
            throw std::runtime_error ("Source / destination invalid");
        }

        if (src == dest)
        {
            throw std::runtime_error ("Source and destination the same");
        }

        if ((entries_.find(src)->second != kRotorContact_end) ||
            (entries_.find(dest)->second != kRotorContact_end))
        {
            throw std::runtime_error ("Source / destination in use");
        }

        entries_.find(src)->second = dest;
        entries_.find(dest)->second = src;
    }

    /*
        Get the opposite end of a plug.If there is a plug then work out the
        other end, otherwise return same letter to represent no plug.

        For example if 'A' is wired to 'T' then 'T' would be returned, but if
        'C' wasn't wired then 'C' is returned.
    */
    RotorContact Plugboard::GetPlug (RotorContact src)
    {
        return (entries_[src] == kRotorContact_end) ? src : entries_[src];
    }

    void Plugboard::Reset ()
    {
        entries_.clear ();

        for (int contact = kRotorContact_A;
            contact != kRotorContact_end;
            contact++)
        {
            entries_.insert ({ (RotorContact)contact, kRotorContact_end });
        }
    }

}   // namespace enigmaSimulator
