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
#include <vector>
#include <stdexcept>
#include <string>
#include "Definitions.h"
#include "IRotorWireConfiguration.h"
#include "Logging.h"
#include "RotorContact.h"

namespace enigmaSimulator {

    using WiringLayout = std::vector<WiringEntry>;

    const std::string DEFAULT_SRC_LAYOUT = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    class RotorWireConfiguration : public IRotorWireConfiguration
    {
    public:
        RotorWireConfiguration () = default;

        RotorWireConfiguration (std::string dest_layout,
            std::string src_layout = DEFAULT_SRC_LAYOUT) : wiring_it_(wiring_.end())
        {
            if (dest_layout.size () != MAX_WIRING_ENTRIES)
            {
                throw std::runtime_error ("Incorrect destination wiring entries!");
            }

            if (src_layout.size () != MAX_WIRING_ENTRIES)
            {
                throw std::runtime_error ("Incorrect source wiring entries!");
            }

            for (int i = 0; i < src_layout.size (); i++)
            {
                RotorContact src = RotorContact ((src_layout.c_str ()[i] - 65) + 1);
                RotorContact dest = RotorContact ((dest_layout.c_str ()[i] - 65) + 1);
                AddEntry (src, dest);
            }
        }

        ~RotorWireConfiguration () = default;

        bool HasValidWiring () { return wiring_.size () == MAX_WIRING_ENTRIES; }

        RotorContact WiringPathForward (const RotorContact src)
        {
            if (!HasValidWiring ()) throw std::runtime_error ("Invalid wiring");

            return wiring_[(static_cast<int>(src) - 1)].dest;
        }

        RotorContact WiringPathReverse (const RotorContact dest)
        {
            if (!HasValidWiring ()) throw std::runtime_error ("Invalid wiring");

            RotorContact src = kRotorContact_end;

            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                if (it->dest == dest)
                {
                    src = it->src;
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

            return { wiring_it_->src, wiring_it_->dest };
        }

        void PrettyPrintSrcWiringPath ()
        {
            TraceLog (kLogLevel_trace, GetSrcWiringPathStr ().c_str ());
        }

        void PrettyPrintDestWiringPath ()
        {
            TraceLog (kLogLevel_trace, GetDestWiringPathStr ().c_str ());
        }

        std::string GetSrcWiringPathStr ()
        {
            std::string wiring;
            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                wiring.push_back ( RotorContactStr[it->src]);
            }

            return wiring;
        }

        std::string GetDestWiringPathStr ()
        {
            std::string wiring;
            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                wiring.push_back (RotorContactStr[it->dest]);
            }

            return wiring;
        }

    private:
        WiringLayout wiring_;
        WiringLayout::iterator wiring_it_;

        void AddEntry (RotorContact src, RotorContact dest)
        {
            for (auto it = wiring_.begin (); it != wiring_.end (); ++it)
            {
                if (it->src == src)
                {
                    throw std::runtime_error ("Duplicate src wiring contact!");
                }

                if (it->dest == dest)
                {
                    throw std::runtime_error ("Duplicate destination wiring contact!");
                }
            }

            wiring_.push_back ( {src, dest} );
        }

    };

}   // namespace enigmaSimulator

#endif  //  #ifndef ROTORWIRINGLAYOUT_H
