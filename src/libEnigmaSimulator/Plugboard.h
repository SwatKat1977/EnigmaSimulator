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
#ifndef PLUGBOARD_H
#define PLUGBOARD_H
#include <map>
#include "RotorContact.h"

namespace enigmaSimulator {

    // Class representing an Enigma plugboard / Steckerbrett.
    class Plugboard
    {
    public:
        Plugboard ();

        ~Plugboard () = default;

        void SetPlug (RotorContact src, RotorContact dest);

        RotorContact GetPlug (RotorContact src);

        void Reset ();

    private:
        std::map<RotorContact, RotorContact> entries_;
    };

}   // namespace enigmaSimulator

#endif  //  #ifndef PLUGBOARD_H
