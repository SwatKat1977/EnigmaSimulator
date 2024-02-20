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
#include <string>
#include "Definitions.h"
#include "IRotorWireConfiguration.h"
#include "RotorContact.h"

namespace enigmaSimulator {

    class RotorWireConfiguration : public IRotorWireConfiguration
    {
    public:

        RotorWireConfiguration () = default;

        RotorWireConfiguration (std::string layout) : wiring_it_(wiring_.end())
        {
            if (layout.size () != MAX_WIRING_ENTRIES)
            {
                throw std::runtime_error ("Incorrect wiring entries!");
            }

            for (int i = 0; i < MAX_WIRING_ENTRIES; i++)
            {
                RotorContact src = RotorContact (i + 1);
                RotorContact dest = RotorContact ((layout.c_str ()[i] - 65) + 1);
                AddEntry (src, dest);
            }
        }

        ~RotorWireConfiguration () = default;

        bool HasValidWiring () { return wiring_.size () == MAX_WIRING_ENTRIES; }

        RotorContact WiringPathForward (const RotorContact src)
        {
            RotorContact destination = kRotorContact_end;

            if (!HasValidWiring ()) throw std::runtime_error ("Invalid wiring");

            return wiring_.find (src)->second;
        }

        RotorContact WiringPathReverse (const RotorContact dest)
        {
            if (!HasValidWiring ()) throw std::runtime_error ("Invalid wiring");

            RotorContact src = kRotorContact_end;

            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                if (it->second == dest)
                {
                    src = it->first;
                }
            }

            return src;
        }

        void FirstWiringPath () { wiring_it_ = wiring_.begin (); }

        void NextWiringPath ()
        {
            if (wiring_it_ != wiring_.end ()) wiring_it_++;
        }

        WiringEntry CurrentWiringPath ()
        {
            if (wiring_it_ == wiring_.end ())
            {
                return { kRotorContact_end, kRotorContact_end };
            }

            return { wiring_it_->first, wiring_it_->second };
        }

    private:
        std::map<RotorContact, RotorContact> wiring_;
        std::map<RotorContact, RotorContact>::iterator wiring_it_;

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

            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                if (it->second == dest)
                {
                    throw std::runtime_error ("Duplicate destination wiring contact!");
                }
            }

            wiring_.insert ({ src, dest });
        }

    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTORWIRINGLAYOUT_H
