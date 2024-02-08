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
#ifndef ENIGMAMACHINETYPE_H
#define ENIGMAMACHINETYPE_H
#include <string>

namespace enigmaSimulator {

    using RotorNamesList = std::vector<std::string>;
    using ReflectorNamesList = std::vector<std::string>;

    // Enumeration for total number of rotors.
    enum RotorCount
    {
        kRotorCount_3 = 3,
        kRotorCount_4 = 4
    };

    // Definition of an Enigma machine tyoe.
    class EnigmaMachineType
    {
    protected:
        bool has_plugboard_;
        std::string long_name_;
        std::string short_name_;
        RotorCount total_rotors_;
        ReflectorNamesList valid_reflectors_;
        RotorNamesList valid_rotors_;

        EnigmaMachineType(
            std::string longName,
            std::string shortName,
            RotorCount totalRotors,
            bool hasPlugboard,
            RotorNamesList valid_rotors,
            ReflectorNamesList valid_reflectors) :
            has_plugboard_(hasPlugboard),
            long_name_(longName),
            short_name_(shortName),
            total_rotors_(totalRotors),
            valid_reflectors_(valid_reflectors),
            valid_rotors_(valid_rotors)
        {
        }

        // Get the long name of the Enigma machine.
        inline std::string LongName() { return long_name_; }

        // Get the short name of the Enigma machine.
        inline std::string ShortName() { return short_name_; }

        // Get the total number of rotors for an Enigma machine.
        inline RotorCount TotalRotors() { return total_rotors_; }

        // Get the Enigma machine has a plugboard flag.
        inline bool HasPlugboard() { return has_plugboard_; }

        // Get the list of available reflectors for the machine.
        ReflectorNamesList reflectors() { return valid_reflectors_; }

        // Get the list of available rotors for the machine.
        RotorNamesList rotors() { return valid_rotors_; }
    };

}   // namespace enigmaSimulator

#endif  //  ENIGMAMACHINETYPE_H
