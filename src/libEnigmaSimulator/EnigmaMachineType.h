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

#ifdef __USE_PY__
class RotorDefintion:
    __slots__ = ['_name', '_notches', '_wiring']

    @property
    def name(self) -> str:
        ''' Get name of rotor. '''
        return self._name

    @property
    def notches(self) -> str:
        ''' Get a list of turnover notches. '''
        return self._notches

    @property
    def wiring(self) -> str:
        ''' Get the rotor wiring. '''
        return self._wiring

    def __init__(self, name: str, wiring : str, notches : list) -> None:
        self._name = name
        self._notches = notches
        self._wiring = wiring

class ReflectorDefinition:
    __slots__ = ['_name', '_wiring']

    @property
    def name(self) -> str:
        ''' Get name of reflector. '''
        return self._name

    @property
    def wiring(self) -> str:
        ''' Get the reflector wiring. '''
        return self._wiring

    def __init__(self, name: str, wiring : str) -> None:
        self._name = name
        self._wiring = wiring

#endif  //  #ifndef __USE_PY__

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
            long_name_(longName), short_name_(shortName),
            total_rotors_(totalRotors), has_plugboard_(hasPlugboard),
            valid_reflectors_(valid_reflectors),
            valid_rotors_(valid_rotors)
        {
        }

        // Get the long name of the Enigma machine.
        inline std::string LongName() { return self._long_name; }

        // Get the short name of the Enigma machine.
        inline std::string ShortName() { return self._short_name; }

        // Get the total number of rotors for an Enigma machine.
        inline RotorCount TotalRotors() { return self._total_rotors; }

        // Get the Enigma machine has a plugboard flag. '''
        inline bool HasPlugboard(self) { return self._has_plugboard; }

        def rotors(self) -> bool:
            ''' Get the list of available rotors for the machine. '''
            return self._rotors

        def reflectors(self) -> bool:
            ''' Get the list of available reflectors for the machine. '''
            return self._reflectors
    };

}   // namespace enigmaSimulator

#endif  //  ENIGMAMACHINETYPE_H
