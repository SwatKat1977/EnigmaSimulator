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
