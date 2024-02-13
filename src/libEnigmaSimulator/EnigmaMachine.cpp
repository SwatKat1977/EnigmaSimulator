/*
    Engima Machine Simulator
    Copyright (C) 2015-2024 Engima Simulator Development Team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
*/
#include <algorithm>
#include <iostream>
#include <memory>
#include "EnigmaMachine.h"
#include "EnigmaMachineTypes.h"
#include "Logging.h"

namespace enigmaSimulator {

    EnigmaMachine::EnigmaMachine() 
        : is_configured_(false),
          lastError_(""),
          plugboard_(nullptr),
          reflector_(nullptr)
    {}

    bool EnigmaMachine::Configure(EnigmaMachineDefinition machineType,
                                  RotorNamesList rotors,
                                  std::string reflectorName)
    {
        type_ = machineType;

        auto modelDetails = ENIGMA_MODELS.find(machineType)->second;

        TraceLog(kLogLevel_info, "Configuring machine...");

        if (rotors.size() != modelDetails.TotalRotors())
        {
            lastError_ = "Invalid number of rotors specified";
            return false;
        }

        RotorPositionNumber position = kRotorPositionNumber_1;
        RotorNamesList validRotors = modelDetails.AllRotors();
        for (auto rotorName = rotors.begin();
             rotorName != rotors.end(); ++rotorName)
        {
            if (std::find(validRotors.begin(),
                          validRotors.end(),
                          (*rotorName)) == validRotors.end())
            {
                lastError_ = "Unknown rotor '" + (*rotorName) + "'";
                return false;
            }

            rotors_.insert ( { position, CreateRotor((*rotorName)) } );
            TraceLog (kLogLevel_info, "Added rotor '%s'", (*rotorName).c_str());
            position = static_cast<RotorPositionNumber>(static_cast<int>(position) + 1);
        }

        if (modelDetails.HasPlugboard())
        {
            TraceLog (kLogLevel_info, "Machine is using a plugboard");
            plugboard_ = new Plugboard();
        }

        ReflectorNamesList validReflectors = modelDetails.AllReflectors();
        if (std::find(validReflectors.begin(),
                      validReflectors.end(),
                      reflectorName) == validReflectors.end())
        {
            lastError_ = "Unknown relector '" + reflectorName + "'";
            return false;
        }

        reflector_ = CreateReflector (reflectorName);
        TraceLog (kLogLevel_info, "Using reflector '%s'", reflectorName.c_str());

        is_configured_ = true;

        return true;
    }

    /*
    To encrypt/decrypt a message, we need to run the key through the enigma
    machine in the following order (for some models plugboard is optional):
    plug board => rotors => reflector => rotors => plugboard.
    @param key Key to encode.
    @return Encoded character.
    */
    RotorContact EnigmaMachine::PressKey(RotorContact key)
    {
        RotorContact currentLetter = key;

        DebugLog( "EnigmaMachine::" + std::string(__func__),
            "received : '%s'", RotorContactStr[key]);

        // To encrypt a key entry it needs to run through the circuit:
        // plug board => rotors => reflector => rotors => plugboard.
        //  The variable currentLetter will maintain the contact state.
        LogRotorStates("=> Rotors before stepping :");

        // Before any encrypting can begin step the rotor.
        StepRotors();

        LogRotorStates("Rotors after stepping :");

        // If a plugboard exists for machine then encode through it.
        if (plugboard_)
        {
            currentLetter = plugboard_->GetPlug(key);
            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "Plugboard | Passed '%s' in and returned '%s'",
                      RotorContactStr[key], RotorContactStr[currentLetter]);
        }

        DebugLog( "EnigmaMachine::" + std::string(__func__),
                  "Passing letter through rotors from right to left");

        // Pass the letter through the rotors from right to left.
        for (auto rotor = rotors_.rbegin (); rotor != rotors_.rend (); ++rotor)
        {
            RotorContact oldLetter = currentLetter;

            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "<===================================================>");
            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "<==== ROTOR '%s' ====>",
                rotor->second->RotorName ().c_str ());
            rotor->second->PrettyPrintWiring();

            // Get substituted letter from each rotor. The returned value will
            // take into account the position of the rotor.
            currentLetter = rotor->second->Encrypt (currentLetter);

            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "Rotor | Passing '%s' returned '%s'",
                RotorContactStr[oldLetter],
                RotorContactStr[currentLetter]);
        }

        // Pass the letter through the reflector.
        RotorContact oldLetter = currentLetter;
        currentLetter = reflector_->Encrypt (currentLetter);
        DebugLog( "EnigmaMachine::" + std::string(__func__),
                  "[Reflector] '%s' => '%s'",
            RotorContactStr[oldLetter], RotorContactStr[currentLetter]);

        DebugLog( "EnigmaMachine::" + std::string(__func__),
                  "Passing letter through rotors from left to right");
        for (auto rotor = rotors_.begin (); rotor != rotors_.end (); ++rotor)
        {
            oldLetter = currentLetter;
            currentLetter = rotor->second->Encrypt (currentLetter, false);

            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "<==== ROTOR '%s' ====>",
                rotor->second->RotorName ().c_str ());
            rotor->second->PrettyPrintWiring();
            DebugLog( "EnigmaMachine::" + std::string(__func__),
                      "Rotor | Passing '%s' returned '%s'",
                RotorContactStr[oldLetter],
                RotorContactStr[currentLetter]);
            rotorOffset = rotor->second->RotorPosition()
                        - kRotorContact_A;
        }

        // If a plugboard exists for machine then encode through it.
        if (plugboard_)
        {
            currentLetter = plugboard_->GetPlug (currentLetter);
        }

        DebugLog( "EnigmaMachine::" + std::string(__func__),
                  "Output letter : '%s'", RotorContactStr[currentLetter]);
        DebugLog( "EnigmaMachine::" + std::string(__func__), 
                  "*********************************************");

        // Return encoded character.
        return currentLetter;
    }

#ifdef __OLD_CODE__

        def set_rotor_position(self, rotor_no : int, position : int) -> None:
            ''' Set the position of the rotor. '''

            # Validate rotor positions.
            if position < 0 or position > 25:
                raise ValueError("Invalid rotor positions")

            if rotor_no < 0 or rotor_no > (len(self._rotors) - 1):
                raise ValueError("Invalid rotor")

            # Set the new rotor position.
            self._rotors[rotor_no].position = position

        def get_rotor_position(self, rotor_no):
            return self._rotors[rotor_no].position
#endif

    /*
    Rotor stepping occurs from the right to left when a stepping notch is hit.
    */
    void EnigmaMachine::StepRotors()
    {
        auto details = ENIGMA_MODELS.find(type_)->second;
        int totalRotors = static_cast<int>(details.TotalRotors());

        // Step next rotor flag.
        bool willStepNextRotor = false;

        // Determine the furthest right rotor (0 indexed list)
        int position = totalRotors -1;

        while( position >= kRotorPositionNumber_1)
        {
            IRotor *rotor = rotors_[RotorPositionNumber(position)];

            if (static_cast<int>(position +1) == details.TotalRotors())
            {
                printf("[TMP] Furthest right rotor....\n");
                //std::cout << "Rotor : " << rotor << std::endl;
                // As the right-hand pawl has no rotor or ring to its right,
                // rotor stepping happens with every key depression.
                //willStepNextRotor = rotor->WillStepNext();
                rotor->Step();
            }
            else
            {
                printf("[TMP] Rotor to step...\n");
                rotor->Step();
            }

#ifdef __IMPLEMENT_DOUBLE_STEP_CODE__   // Code to be ported
            # If there is a double-step then perform it and reset the flag.
            if self._double_step:
                print("[DEBUG] Doing a double step")
                self._rotors[0].step()
                self._rotors[1].step()
                self._double_step = False
#endif  //  #ifdef __IMPLEMENT_DOUBLE_STEP_CODE__

            // Only continue if there is more stepping to be done.
            if (!willStepNextRotor) return;

#ifdef __IMPLEMENT_DOUBLE_STEP_CODE__   // Code to be ported
            # If the 2nd rotor will step rotor 1 (left most one) then a double-step
            # needs to take place.  This is where the middle rotor will step again
            # next button press, along with the left one.
            if rotor.will_step_next():
                self._double_step = True
#endif  //  #ifdef __IMPLEMENT_DOUBLE_STEP_CODE__

            position = position -= 1;
        }
    }

    void EnigmaMachine::LogRotorStates(std::string prefix)
    {
#ifdef __OLD_CODE__
        rotor_0 = RotorContact(self._rotors[0].position).name
        rotor_1 = RotorContact(self._rotors[1].position).name
        rotor_2 = RotorContact(self._rotors[2].position).name
        self._logger.log_debug(f"{prefix_str} {rotor_0} | {rotor_1} | " + \
                               f"{rotor_2}")
#endif
    }

    IRotor *EnigmaMachine::GetRotor(RotorPositionNumber position)
    {
        auto modelDetails = ENIGMA_MODELS.find(type_)->second;

        if (static_cast<int>(position) >=
            static_cast<int>(modelDetails.TotalRotors()))
        {
            return nullptr;
        }

        return rotors_[position];
    }

}   // namespace enigmaSimulator
