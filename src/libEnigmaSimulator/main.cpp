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
#include "Logging.h"

void LogDebugMessage(std::string functionName, std::string msg, bool clipped)
{
    std::cout << "[DEBUG] " << functionName << "() " << msg << std::endl;
}

void LogDebugMessage(enigmaSimulator::LogLevel level,
    std::string msg, bool clipped)
{
    std::string levelStr = ((level == enigmaSimulator::kLogLevel_info))
        ? "INFO" : "TRACE";
    std::cout << "[" << levelStr << "] " << msg << std::endl;
}

int main (int argc, char** argv)
{
    enigmaSimulator::AssignLoggingDebugCallback(LogDebugMessage);
    enigmaSimulator::AssignLoggingTraceCallback(LogDebugMessage);

    auto machine = enigmaSimulator::EnigmaMachine();
    bool status = machine.Configure(
        enigmaSimulator::kEnigmaMachineDefinition_EnigmaModelM3,
        enigmaSimulator::RotorNamesList { "EnigmaM3_I", "EnigmaM3_II", "EnigmaM3_III"},
        "EnigmaM3_Reflector_UKW-B");

    if (!status)
    {
        std::cout << "Last error : " << machine.LastError () << std::endl;
        return 0;
    }

    std::cout << "Left Rotor : "
              << machine.GetRotor(enigmaSimulator::kRotorPositionNumber_1)->RotorName()
              << std::endl;
    std::cout << "Middle Rotor : "
              << machine.GetRotor(enigmaSimulator::kRotorPositionNumber_2)->RotorName()
              << std::endl;
    std::cout << "Right Rotor : "
              << machine.GetRotor(enigmaSimulator::kRotorPositionNumber_3)->RotorName()
              << std::endl;

    std::cout << "ENCODED 'A' : "
              << enigmaSimulator::RotorContactStr[machine.PressKey(enigmaSimulator::kRotorContact_A)]
              << std::endl;
    std::cout << "ENCODED 'A' : "
              << enigmaSimulator::RotorContactStr[machine.PressKey(enigmaSimulator::kRotorContact_A)]
              << std::endl;
    std::cout << "ENCODED 'A' : "
              << enigmaSimulator::RotorContactStr[machine.PressKey(enigmaSimulator::kRotorContact_A)]
              << std::endl;

    return 0;
}
