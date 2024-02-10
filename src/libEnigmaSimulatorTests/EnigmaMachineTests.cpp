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
#include "gtest/gtest.h"
#include "EnigmaMachine.h"
#include "EnigmaMachineTest.h"

TEST_F(EnigmaMachineTest, ConfigureIncorrectRotors)
{
    bool status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_II"},
        "Enigma1_Reflector_UKW-A");

    EXPECT_FALSE(status) << "Expecting configuration to return false";
    EXPECT_EQ(machine_.LastError(), "Invalid number of rotors specified");
    EXPECT_FALSE(machine_.IsConfigured());
}

TEST_F(EnigmaMachineTest, ConfigureUnknownRotor)
{
    bool status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_A", "Enigma1_II", "Enigma1_III"},
        "Enigma1_Reflector_UKW-A");
    EXPECT_FALSE(status) << "Expecting configuration to return false";
    EXPECT_EQ(machine_.LastError(), "Unknown rotor 'Enigma1_A'");
    EXPECT_FALSE(machine_.IsConfigured());

    status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_B", "Enigma1_III"},
        "novalue");
    EXPECT_FALSE(status) << "Expecting configuration to return false";
    EXPECT_EQ(machine_.LastError(), "Unknown rotor 'Enigma1_B'");
    EXPECT_FALSE(machine_.IsConfigured());

    status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_II", "Enigma1_C"},
        "Enigma1_Reflector_UKW-A");
    EXPECT_FALSE(status) << "Expecting configuration to return false";
    EXPECT_EQ(machine_.LastError(), "Unknown rotor 'Enigma1_C'");
    EXPECT_FALSE(machine_.IsConfigured());
}

TEST_F(EnigmaMachineTest, ConfigureVerifyPlugboard)
{
    bool status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_II", "Enigma1_III"},
        "Enigma1_Reflector_UKW-A");
    EXPECT_TRUE(status) << "Expecting configuration to return true (success)";
    EXPECT_NE(machine_.MachinePlugboard(), nullptr) << "Plugboard should not be nullptr";
    EXPECT_EQ(machine_.LastError(), "");
    EXPECT_TRUE(machine_.IsConfigured());
}

TEST_F(EnigmaMachineTest, ConfigureUnknownReflector)
{
    bool status = machine_.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_II", "Enigma1_III"},
        "This is invalid");
    EXPECT_FALSE(status) << "Expecting configuration to return false (unsuccess)";
    EXPECT_EQ(machine_.LastError(), "Unknown relector 'This is invalid'");
    EXPECT_FALSE(machine_.IsConfigured());
}
