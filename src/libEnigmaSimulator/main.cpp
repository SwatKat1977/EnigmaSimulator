#include <iostream>
#include "RotorContact.h"
#include "RotorWiringLayout.h"
#include "Rotor.h"

int main (int argc, char** argv)
{
    enigmaSimulator::RotorWiringLayout wiringLayout;

    // EKMFLGDQVZNTOWYHXUSPAIBRCJ

    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_A, enigmaSimulator::kRotorContact_E);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_B, enigmaSimulator::kRotorContact_K);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_C, enigmaSimulator::kRotorContact_M);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_D, enigmaSimulator::kRotorContact_F);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_E, enigmaSimulator::kRotorContact_L);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_F, enigmaSimulator::kRotorContact_G);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_G, enigmaSimulator::kRotorContact_D);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_H, enigmaSimulator::kRotorContact_Q);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_I, enigmaSimulator::kRotorContact_V);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_J, enigmaSimulator::kRotorContact_Z);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_K, enigmaSimulator::kRotorContact_N);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_L, enigmaSimulator::kRotorContact_T);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_M, enigmaSimulator::kRotorContact_O);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_N, enigmaSimulator::kRotorContact_W);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_O, enigmaSimulator::kRotorContact_Y);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_P, enigmaSimulator::kRotorContact_H);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_Q, enigmaSimulator::kRotorContact_X);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_R, enigmaSimulator::kRotorContact_U);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_S, enigmaSimulator::kRotorContact_S);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_T, enigmaSimulator::kRotorContact_P);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_U, enigmaSimulator::kRotorContact_A);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_V, enigmaSimulator::kRotorContact_I);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_W, enigmaSimulator::kRotorContact_B);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_X, enigmaSimulator::kRotorContact_R);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_Y, enigmaSimulator::kRotorContact_C);
    wiringLayout.AddEntry (enigmaSimulator::kRotorContact_Z, enigmaSimulator::kRotorContact_J);

    auto rotor = enigmaSimulator::Rotor("Rotor 1", wiringLayout, std::vector<enigmaSimulator::RotorContact>());

    rotor.RotorPosition(enigmaSimulator::kRotorContact_B);

    auto test1 = rotor.Encrypt(enigmaSimulator::kRotorContact_A);
    printf("[Test 1] 'A' in position 'B' pressed and we got '%s' (%d)\n",
           enigmaSimulator::RotorContactStr[test1], test1);

    rotor.RotorPosition(enigmaSimulator::kRotorContact_D);
    auto test2 = rotor.Encrypt(enigmaSimulator::kRotorContact_X);
    printf("[Test 1] 'X' pressed and we got '%s' (%d)\n",
           enigmaSimulator::RotorContactStr[test2], test2);

    return 0;
}
