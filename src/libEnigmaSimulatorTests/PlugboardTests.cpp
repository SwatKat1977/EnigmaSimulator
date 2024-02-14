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
#include "PlugboardTest.h"

TEST_F(PlugboardTest, SetPlugValid)
{
    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_A,
            enigmaSimulator::kRotorContact_B);
    }
    catch(const std::runtime_error &e)
    {
        std::cout << "SetPlugValid : " << e.what() << std::endl;
        FAIL() << "Unexpectected std::runtime_error exception";
    }
}

TEST_F(PlugboardTest, SetPlugInvalidPlug)
{
    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_end,
            enigmaSimulator::kRotorContact_A);
        FAIL() << "Expectecting std::runtime_error exception";
    }
    catch(const std::runtime_error &e)
    {
        EXPECT_STREQ(e.what(), "Source / destination invalid");
    }

    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_A,
            enigmaSimulator::kRotorContact_end);
        FAIL() << "Expectecting std::runtime_error exception";
    }
    catch(const std::runtime_error &e)
    {
        EXPECT_STREQ(e.what(), "Source / destination invalid");
    }
}

TEST_F(PlugboardTest, SetPlugSrcDestSame)
{
    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_T,
            enigmaSimulator::kRotorContact_T);
        FAIL() << "Expectecting std::runtime_error exception";
    }
    catch(const std::runtime_error &e)
    {
        EXPECT_STREQ(e.what(), "Source and destination the same");
    }
}

TEST_F(PlugboardTest, SetPlugInUse)
{
    plugboard_.SetPlug(
        enigmaSimulator::kRotorContact_A,
        enigmaSimulator::kRotorContact_Z);
    plugboard_.SetPlug(
        enigmaSimulator::kRotorContact_Y,
        enigmaSimulator::kRotorContact_B);

    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_A,
            enigmaSimulator::kRotorContact_T);
        FAIL() << "Expectecting std::runtime_error exception";
    }
    catch(const std::runtime_error &e)
    {
        EXPECT_STREQ(e.what(), "Source / destination in use");
    }

    try
    {
        plugboard_.SetPlug(
            enigmaSimulator::kRotorContact_D,
            enigmaSimulator::kRotorContact_Y);
        FAIL() << "Expectecting std::runtime_error exception";
    }
    catch(const std::runtime_error &e)
    {
        EXPECT_STREQ(e.what(), "Source / destination in use");
    }
}

TEST_F(PlugboardTest, GetPlugUsedPlug)
{
    plugboard_.SetPlug(
        enigmaSimulator::kRotorContact_A,
        enigmaSimulator::kRotorContact_Z);

    // Forward GetPlug()
    auto plug = plugboard_.GetPlug(enigmaSimulator::kRotorContact_A);
    EXPECT_EQ(plug, enigmaSimulator::kRotorContact_Z);

    // Reverse GetPlug()
    plug = plugboard_.GetPlug(enigmaSimulator::kRotorContact_Z);
    EXPECT_EQ(plug, enigmaSimulator::kRotorContact_A);
}

TEST_F(PlugboardTest, GetPlugUnusedPlug)
{
    plugboard_.SetPlug(
        enigmaSimulator::kRotorContact_A,
        enigmaSimulator::kRotorContact_Z);

    auto plug = plugboard_.GetPlug(enigmaSimulator::kRotorContact_G);
    EXPECT_EQ(plug, enigmaSimulator::kRotorContact_G);
}
