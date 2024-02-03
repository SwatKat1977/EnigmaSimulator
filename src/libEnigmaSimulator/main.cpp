#include <iostream>
#include "RotorContact.h"
#include "RotorWiringLayout.h"

int main (int argc, char** argv)
{
    enigmaSimualator::RotorWiringLayout wiringLayout;

    // EKMFLGDQVZNTOWYHXUSPAIBRCJ

    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_A, enigmaSimualator::kRotorContact_E);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_B, enigmaSimualator::kRotorContact_K);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_C, enigmaSimualator::kRotorContact_M);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_D, enigmaSimualator::kRotorContact_F);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_E, enigmaSimualator::kRotorContact_L);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_F, enigmaSimualator::kRotorContact_G);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_G, enigmaSimualator::kRotorContact_D);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_H, enigmaSimualator::kRotorContact_Q);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_I, enigmaSimualator::kRotorContact_V);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_J, enigmaSimualator::kRotorContact_Z);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_K, enigmaSimualator::kRotorContact_N);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_L, enigmaSimualator::kRotorContact_T);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_M, enigmaSimualator::kRotorContact_O);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_N, enigmaSimualator::kRotorContact_W);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_O, enigmaSimualator::kRotorContact_Y);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_P, enigmaSimualator::kRotorContact_H);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_Q, enigmaSimualator::kRotorContact_X);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_R, enigmaSimualator::kRotorContact_U);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_S, enigmaSimualator::kRotorContact_S);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_T, enigmaSimualator::kRotorContact_P);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_U, enigmaSimualator::kRotorContact_A);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_V, enigmaSimualator::kRotorContact_I);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_W, enigmaSimualator::kRotorContact_B);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_X, enigmaSimualator::kRotorContact_R);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_Y, enigmaSimualator::kRotorContact_C);
    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_Z, enigmaSimualator::kRotorContact_J);

    ///////    wiringLayout.AddEntry (enigmaSimualator::kRotorContact_A, enigmaSimualator::kRotorContact_E);

    printf("Is Valid? : %d\n", wiringLayout.IsValid());

    printf("DEST of A : %d\n", wiringLayout.GetDestination(enigmaSimualator::kRotorContact_A));
    printf("DEST of Z : %d\n", wiringLayout.GetDestination(enigmaSimualator::kRotorContact_Z));

    std::cout << "A convert : "
              << enigmaSimualator::RotorContactStr[enigmaSimualator::kRotorContact_A]
              << std::endl;

    std::cout << "Z convert : "
              << enigmaSimualator::RotorContactStr[enigmaSimualator::kRotorContact_Z]
              << std::endl;

    return 0;
}
