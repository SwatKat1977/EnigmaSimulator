#include "gtest/gtest.h"
#include "Rotor.h"
#include "RotorTest.h"

int cubic(int pop)
{
    return 0;
}

TEST_F(RotorTest, ConstructWithValidWiring)
{
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

TEST_F(RotorTest, EncryptNoRotorRingOrPositionOffsets)
{
    auto rotor = enigmaSimulator::Rotor(
        "Rotor 1",
        valid_wiring_layout_,
        std::vector<enigmaSimulator::RotorContact>());

    auto output = rotor.Encrypt(enigmaSimulator::kRotorContact_A);

    ASSERT_EQ(output, enigmaSimulator::kRotorContact_E);
}

int main(int argc, char **argv)
{
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
