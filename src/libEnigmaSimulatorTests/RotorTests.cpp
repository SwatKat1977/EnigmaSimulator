#include "gtest/gtest.h"
#include "Rotor.h"
#include "RotorTest.h"

int cubic(int pop)
{
    return 0;
}

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

    auto output = rotor.Encrypt(enigmaSimulator::kRotorContact_A);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_E);
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

    rotor.RotorPosition(enigmaSimulator::kRotorContact_B);
    auto output = rotor.Encrypt(enigmaSimulator::kRotorContact_A);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_J);

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
    output = rotor.Encrypt(enigmaSimulator::kRotorContact_A);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_B);

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
    output = rotor.Encrypt(enigmaSimulator::kRotorContact_X);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_B)
        << "Expected 'B', got '"
        << enigmaSimulator::RotorContactStr[output] << "'";
}
