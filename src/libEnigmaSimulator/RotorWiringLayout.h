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

    const int MAX_WIRING_ENTRIES = 26;

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

            if (wiring_.find (src) != wiring_.end ())
            {
                throw std::runtime_error ("Duplicate source wiring contact!");
            }

            for (auto it = wiring_.begin(); it != wiring_.end(); ++it)
            {
                if (it->second == dest)
                {
                throw std::runtime_error ("Duplicate destination wiring contact!");
                }
            }

            wiring_.insert( {src, dest} );
        }

        bool IsValid()
        {
            return wiring_.size () == MAX_WIRING_ENTRIES;
        }

        // Get destination end of contact, if the wiring isn't valid then an
        // invalid contact (kRotorContact_end) is returned.
        RotorContact GetDestination(const RotorContact src, bool forward = true)
        {
            RotorContact destination = kRotorContact_end;

            if (IsValid())
            {
                if (forward)
                {
                    destination = wiring_.find(src)->second;
                }
                else
                {
                    for (auto it = wiring_.begin(); it != wiring_.end(); ++it)
                    {
                        if (it->second == src)
                        {
                            destination = it->first;
                        }
                    }
                }
            }

            return destination;
        }

    private:
        std::map<RotorContact, RotorContact> wiring_;
    };

}   // namespace enigmaSimualator

#endif  //  #ifndef ROTORWIRINGLAYOUT_H
