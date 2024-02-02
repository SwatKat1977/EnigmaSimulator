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
#ifndef ROTORWIRINGLAYOUT_H
#define ROTORWIRINGLAYOUT_H
#include <map>
#include <stdexcept>
#include "RotorContact.h"

namespace enigmaSimualator {

    const int MAX_WIRING_ENTRIES = 25;

    class RotorWiringLayout
    {
    public:
        RotorWiringLayout () = default;

        ~RotorWiringLayout () = default;

        void AddEntry (RotorContact src, RotorContact dest)
        {
            if (wiring_.size () == MAX_WIRING_ENTRIES)
            {
                throw std::runtime_error ("Too many wiring entries!");
            }

            auto srcSearch = wiring_.find (src);
            auto destSearch = wiring_.find (dest);
            if (srcSearch != wiring_.end () || destSearch != wiring_.end ())
            {
                throw std::runtime_error ("Duplicate wiring entries!");
            }
            /*
            for (auto it = someMap.begin(); it != someMap.end(); ++it)
    if (it->second == someValue)
        return it->first;
            */
        }

    private:
        std::map<RotorContact, RotorContact> wiring_;
    };

}   // namespace enigmaSimualator

#endif  //  #ifndef ROTORWIRINGLAYOUT_H
