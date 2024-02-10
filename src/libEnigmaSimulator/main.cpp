#include <iostream>
#include "EnigmaMachineType.h"
#include "RotorContact.h"
#include "RotorWiringLayout.h"
#include "Reflector.h"
#include "Rotor.h"
#include "Version.h"
#include "RotorFactory.h"
#include "EnigmaMachineTypes.h"
#include "EnigmaMachine.h"

int main (int argc, char** argv)
{
    auto machine = enigmaSimulator::EnigmaMachine();
    bool status = machine.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_Enigma1,
        enigmaSimulator::RotorNamesList { "Enigma1_I", "Enigma1_II", "Enigma1_III"},
        "Enigma1_Reflector_UKW-A");

    if (!status)
    {
        std::cout << "Last error : " << machine.LastError () << std::endl;
    }

    machine.PressKey(enigmaSimulator::kRotorContact_A);

    return 0;
}
