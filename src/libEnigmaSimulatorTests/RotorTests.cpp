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
#include "Rotor.h"
#include "RotorTest.h"

TEST_F(RotorTest, ConstructWithValidWiring)
{
    /*
    Test construction of rotor with an valid wiring layout, it should result
    in the construction of a rotor object.
    */
    try
    {
        auto rotor = enigmaSimulator::Rotor(
            "Rotor 1",
            valid_wiring_layout_,
            std::vector<enigmaSimulator::RotorContact>());
    }
    catch(const std::exception& e)
    {
        FAIL() << "Expected valid rotor wiring";
    }
}

TEST_F(RotorTest, ConstructWithInvalidWiring)
{
    /*
    Test construction of rotor with an invalid wiring layout, it should result
    in a std::runtime_error being thrown with the description text of 
    'Wiring layout is not valid'.
    */
    try
    {
        auto rotor = enigmaSimulator::Rotor(
            "Rotor 1",
            invalid_wiring_layout_,
            std::vector<enigmaSimulator::RotorContact>());
        FAIL() << "Expected invalid rotor wiring";
    }
    catch(const std::exception& e)
    {
    }
}

TEST_F(RotorTest, EncryptNoPositionOrRingOffset)
{
    /*
    Test encrypting a letter, the parameters are:
    => Encrypted Char : 'A'
    => Rotor Position : 0
    => Ring Offset    : 0

    The letter 'A' is wired to the letter 'E'. since neither the rotors
    position, or the ring offset  have been changed it should return 'E'.
    */
    auto rotor = enigmaSimulator::Rotor(
        "Rotor 1",
        valid_wiring_layout_,
        std::vector<enigmaSimulator::RotorContact>());

    auto output = rotor.EncryptForward(enigmaSimulator::kRotorContact_A);
    EXPECT_EQ(output, enigmaSimulator::kRotorContact_E)
        << "Expecting 'E', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";

    output = rotor.EncryptReverse(enigmaSimulator::kRotorContact_A);
    EXPECT_EQ(output, enigmaSimulator::kRotorContact_U)
        << "Expecting 'E', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";
}

TEST_F(RotorTest, EncryptPositionChangedSimpleNoRingOffset)
{
    /*
    Test encrypting a letter with a simple position change, the position is
    moved forward 1. Test 1 parameters are:
    => Encrypted Char : 'A'
    => Rotor Position : B
    => Ring Offset    : 0

    The letter 'A' is wired to the letter 'E'. since the rotor position is now
    at position 'B', 'A' enters in the 'B' position which is wired to 'K', but
    on the way out it is at a -1 position, therefore 'J' is returned.
    */
    auto rotor = enigmaSimulator::Rotor(
        "Rotor 1",
        valid_wiring_layout_,
        std::vector<enigmaSimulator::RotorContact>());

    // Forward test
    rotor.RotorPosition(enigmaSimulator::kRotorContact_B);
    auto output = rotor.EncryptForward(enigmaSimulator::kRotorContact_A);
    EXPECT_EQ(output, enigmaSimulator::kRotorContact_J)
        << "Expecting 'J', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";

    // Reverse test
    output = rotor.EncryptReverse(enigmaSimulator::kRotorContact_H);
    EXPECT_EQ(output, enigmaSimulator::kRotorContact_U)
        << "From 'I' expecting 'U', got " << enigmaSimulator::RotorContactStr[output];


    /*
    Test encrypting a letter with a longer position change, the position is
    moved forward 6. Test 2 parameters are:
    => Encrypted Char : 'A'
    => Rotor Position : F
    => Ring Offset    : 0

    The letter 'A' is wired to the letter 'E'. since the rotor position is now
    at position 'F', 'A' enters in the 'F' position which is wired to 'G', but
    on the way out it is offset -5 positions, therefore 'B' is returned.
    */
    rotor.RotorPosition(enigmaSimulator::kRotorContact_F);
    output = rotor.EncryptForward(enigmaSimulator::kRotorContact_A);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_B)
        << "Expecting 'B', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";

    /*
    Test encrypting a letter where the position change overflows. The letter
    'X' is to be encrypted, the rotoe position is 'D', moving forward 4 steps.
    Test 3 parameters are:
    => Encrypted Char : 'X'
    => Rotor Position : D
    => Ring Offset    : 0

    The letter 'X' is wired to the letter 'R'. since the rotor position is now
    at position 'D', 'X' enters in the 'D' position meaning +4 is added to the
    rotor, therefore entering at 'B' which is wired to 'G', but
    on the way out it is at a -6 position, therefore 'B' is returned.
    */
    rotor.RotorPosition(enigmaSimulator::kRotorContact_D);
    output = rotor.EncryptForward(enigmaSimulator::kRotorContact_X);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_B)
        << "Expected 'B', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";
}

/*
    test : will_step_next()
        # Test will not step.
        assertEqual : rotor.will_step_next(), False

        # Test will step.
        rotor.position = RotorContact.Q.value
        assertEqual : rotor.will_step_next(), true

    test :step
        # Simple step test from positioh 1 to 2.
        self.assertEqual(self._valid_pass_through_rotor.position, 0)
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 1)

        # Step test from position 25 (Z) to 1 (A).
        self._valid_pass_through_rotor.position = 25
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 1)
*/

TEST_F(RotorTest, EncryptNoPositionChangedHasRingOffset)
{
    auto rotor = enigmaSimulator::Rotor(
        "Rotor 1",
        valid_wiring_layout_,
        std::vector<enigmaSimulator::RotorContact>());

    // Forward test 1 / 2
    rotor.RingPosition(enigmaSimulator::kRotorContact_C);
    auto fwdOut1 = rotor.EncryptForward(enigmaSimulator::kRotorContact_G);
    EXPECT_EQ(fwdOut1, enigmaSimulator::kRotorContact_N)
        << "From 'G' expecting 'N', got " << enigmaSimulator::RotorContactStr[fwdOut1];

    // Forward test 2 / 2
    rotor.RingPosition(enigmaSimulator::kRotorContact_Z);
    auto fwdOut2 = rotor.EncryptForward(enigmaSimulator::kRotorContact_K);
    EXPECT_EQ(fwdOut2, enigmaSimulator::kRotorContact_S)
        << "From 'K' expecting 'S', got " << enigmaSimulator::RotorContactStr[fwdOut2];

    // Reverse test
    rotor.RingPosition(enigmaSimulator::kRotorContact_C);
    auto revOut1 = rotor.EncryptReverse(enigmaSimulator::kRotorContact_C);
    EXPECT_EQ(revOut1, enigmaSimulator::kRotorContact_W)
        << "From 'C' expecting 'W', got '"
        << enigmaSimulator::RotorContactStr[revOut1] << "'";
}

TEST_F(RotorTest, EncryptPositionChangedHasRingOffset)
{
    auto rotor = enigmaSimulator::Rotor(
    "Rotor 1",
    valid_wiring_layout_,
    std::vector<enigmaSimulator::RotorContact>());

    // Forward test 1
    rotor.RingPosition(enigmaSimulator::kRotorContact_C);
    rotor.RotorPosition(enigmaSimulator::kRotorContact_G);
    auto fwdOut = rotor.EncryptForward(enigmaSimulator::kRotorContact_G);
    EXPECT_EQ(fwdOut, enigmaSimulator::kRotorContact_J)
        << "Pressed 'G' : Ring: 'C' From 'G' expecting 'J', got "
        << enigmaSimulator::RotorContactStr[fwdOut];

    // Reverse test
    rotor.RingPosition(enigmaSimulator::kRotorContact_C);
    rotor.RotorPosition(enigmaSimulator::kRotorContact_C);

    auto revOut = rotor.EncryptReverse(enigmaSimulator::kRotorContact_W);
    EXPECT_EQ(revOut, enigmaSimulator::kRotorContact_N)
        << "Pressed 'W' : Ring: 'C' From 'C' expecting 'N', got "
        << enigmaSimulator::RotorContactStr[revOut];
}
