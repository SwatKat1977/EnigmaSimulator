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

void LogTraceMessage(enigmaSimulator::LogLevel level,
    std::string msg, bool clipped)
{
    std::string levelStr = ((level == enigmaSimulator::kLogLevel_info))
        ? "INFO" : "TRACE";
    std::cout << "[" << levelStr << "] " << msg << std::endl;
}

int main (int argc, char** argv)
{
    bool enableDebug = false;
    bool enableTrace = false;

    for (auto i = 1; i < argc; ++i)
    {
        if (strcmp(argv[i], "/d") == 0) enableDebug = true;
        if (strcmp(argv[i], "/t") == 0) enableTrace = true;
    }

    if (enableDebug)
    {
        std::cout << "Assigning debug callback" << std::endl;
        enigmaSimulator::AssignLoggingDebugCallback(LogDebugMessage);
    }

    if (enableTrace)
    {
        std::cout << "Assigning trace callback" << std::endl;
        enigmaSimulator::AssignLoggingTraceCallback(LogTraceMessage);
    }

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

    enigmaSimulator::RotorContact output;
    output = machine.PressKey(enigmaSimulator::kRotorContact_A);
    std::cout << "Pressed Letter 'A' | Output : " <<
        enigmaSimulator::RotorContactStr[output] << std::endl;

    output = machine.PressKey(enigmaSimulator::kRotorContact_A);
    std::cout << "Pressed Letter 'A' | Output : " <<
        enigmaSimulator::RotorContactStr[output] << std::endl;

    output = machine.PressKey(enigmaSimulator::kRotorContact_A);
    std::cout << "Pressed Letter 'A' | Output : " <<
        enigmaSimulator::RotorContactStr[output] << std::endl;

    return 0;
}
