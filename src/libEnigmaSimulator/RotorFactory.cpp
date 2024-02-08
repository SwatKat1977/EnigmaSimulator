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
const std::string ENIGMA_M3 = "EnigmaM3_";
const std::string ENIGMA_M4 = "EnigmaM4_";

RotorsMap ROTORS =
{
    // Enigma I
    { ENIGMA_1 + "I",   { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Y" } },
    { ENIGMA_1 + "II",  { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "M" } },
    { ENIGMA_1 + "III", { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "D" } },
    { ENIGMA_1 + "IV",  { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "R" } },
    { ENIGMA_1 + "V",   { "VZBRGITYUPSDNHLXAWMJQOFECK", "H" } },

    // Enigma Model M3
    { ENIGMA_M3 + "I",    { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q" } },
    { ENIGMA_M3 + "II",   { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E" } },
    { ENIGMA_M3 + "III",  { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V" } },
    { ENIGMA_M3 + "IV",   { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J" } },
    { ENIGMA_M3 + "V",    { "VZBRGITYUPSDNHLXAWMJQOFECK", "Z" } },
    { ENIGMA_M3 + "VI",   { "JPGVOUMFYQBENHZRDKASXLICTW", "ZM" } },
    { ENIGMA_M3 + "VII",  { "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM" } },
    { ENIGMA_M3 + "VIII", { "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM" } },

    // German Navy 4-rotor M4 Enigma
    { ENIGMA_M4 + "I",    { "EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q" } },
    { ENIGMA_M4 + "II",   { "AJDKSIRUXBLHWTMCQGZNPYFVOE", "E" } },
    { ENIGMA_M4 + "III",  { "BDFHJLCPRTXVZNYEIWGAKMUSQO", "V" } },
    { ENIGMA_M4 + "IV",   { "ESOVPZJAYQUIRHXLNFTGKDCMWB", "J" } },
    { ENIGMA_M4 + "V",    { "VZBRGITYUPSDNHLXAWMJQOFECK", "Z" } },
    { ENIGMA_M4 + "VI",   { "JPGVOUMFYQBENHZRDKASXLICTW", "ZM" } },
    { ENIGMA_M4 + "VII",  { "NZJHGRCXMYSWBOUFAIVLPEKQDT", "ZM" } },
    { ENIGMA_M4 + "VIII", { "FKQHTLXOCBJSPDZRAMEWNIUYGV", "ZM" } }
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
