#include <map>
#include <string>
#include "RotorFactory.h"
#include "RotorWiringLayout.h"

namespace enigmaSimulator {

struct RotorEntry
{
    std::string layout;
    std::string notches;
};

using RotorsMap = std::map<std::string, RotorEntry>;
const std::string ENIGMA_1 = "Enigma1_";
RotorsMap ROTORS =
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
    RotorsMap::iterator it = ROTORS.find(rotorName);

    if (it == ROTORS.end())
    {
        return nullptr;
    }

    RotorEntry entry = it->second;

    std::vector<RotorContact> notches;

    if (entry.notches.size())
    {
        for (int i = 0; i < entry.notches.size(); i++)
        {
            auto notch = RotorContact((entry.notches.c_str()[i] -65) +1);
            notches.push_back(notch);
        }
    }

    return new Rotor(
        rotorName,
        RotorWiringLayout(entry.layout),
        notches);
}

}   // namespace enigmaSimulator
