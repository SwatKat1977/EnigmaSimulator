#include <map>
#include <string>
#include "RotorFactory.h"

namespace enigmaSimulator {

struct RotorEntry
{
    std::string layout;
    std::string notches;
};

const std::string ENIGMA_1 = "Enigma1_";
const std::map<std::string, RotorEntry> ROTORS =
{
    // Enigma I
    { ENIGMA_1 + "I",   { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Y" } },
    { ENIGMA_1 + "II",  { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "M" } },
    { ENIGMA_1 + "III", { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "D" } },
    { ENIGMA_1 + "IV",  { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "R" } },
    { ENIGMA_1 + "V",   { "VZBRGITYUPSDNHLXAWMJQOFECK", "H" } }
};

Rotor *CreateRotor(std::string rotorName)
{
    return nullptr;
}

}   // namespace enigmaSimulator
