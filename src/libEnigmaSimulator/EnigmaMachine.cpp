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

        DEBUG_LOG("Configuring machine...\n")

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
            DEBUG_LOG("Added rotor '%s'\n", (*rotorName).c_str())
            position = static_cast<RotorPositionNumber>(static_cast<int>(position) + 1);
        }

        if (modelDetails.HasPlugboard())
        {
            DEBUG_LOG("Machine is using a plugboard\n")
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
        DEBUG_LOG("Using reflector '%s'\n", reflectorName.c_str())

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

        DEBUG_LOG("EnigmaMachine::press_key() received : '%s'\n",
            RotorContactStr[key])

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
            DEBUG_LOG("Plugboard | Passed '%s' in and returned '%s'\n",
                      RotorContactStr[key], RotorContactStr[currentLetter])
        }

        DEBUG_LOG("Passing letter through rotors from right to left\n")

        // Pass the letter through the rotors from right to left.
        for (auto rotor = rotors_.rbegin (); rotor != rotors_.rend (); ++rotor)
        {
            RotorContact oldLetter = currentLetter;

            // Get substituted letter from each rotor. The returned value will
            // take into account the position of the rotor.
            currentLetter = rotor->second->Encrypt (currentLetter);

            DEBUG_LOG ("<==== ROTOR '%s' ====>\n",
                rotor->second->RotorName ().c_str ())
            DEBUG_LOG ("Rotor | Passing '%s' to %s returned '%s'\n",
                RotorContactStr[oldLetter],
                rotor->second->RotorName().c_str(),
                RotorContactStr[currentLetter])
        }

        // Pass the letter through the reflector.
        RotorContact oldLetter = currentLetter;
        currentLetter = reflector_->Encrypt (currentLetter);
        DEBUG_LOG ("[Reflector] '%s' => '%s'\n",
            RotorContactStr[oldLetter], RotorContactStr[currentLetter]);

#ifdef __OLD_CODE__
        self._logger.log_debug ("Passing letter through rotors from left to right");

        # Pass the letter through the rotors from left to right.
        for rotor in self._rotors:
            old_letter = RotorContact(current_letter).name
            current_letter = rotor.encrypt(current_letter, forward=False)

            debug_msg = f"Passing '{old_letter}' to {rotor.name} =>" + \
                        f"'{RotorContact(current_letter).name}'"
            self._logger.log_debug(debug_msg)

        # If a plugboard exists for machine then encode through it.
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(current_letter)

        self._logger.log_debug(f"Output letter '{current_letter.name}'")
        self._logger.log_debug("*********************************************")

#endif

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

    void EnigmaMachine::StepRotors()
    {
#ifdef __OLD_CODE__
        '''
        Rotor stepping occurs from the right to left whilst a stepping
        notch is encountered.
        '''

        # Step next rotor flag.
        will_step_next_rotor = False

        ######################################
        ### Assume 3 rotor machine for now ###
        ######################################
        no_of_rotors = 3

        # Determine the furthest right rotor (0 indexed list)
        rotor_position = no_of_rotors -1

        # Because the right-hand pawl has no rotor or ring to its right, rotor
        # stepping happens with every key depression.
        rotor = self._rotors[rotor_position]
        will_step_next_rotor = rotor.will_step_next()
        rotor.step()

        # If there is a double-step then perform it and reset the flag.
        if self._double_step:
            print("[DEBUG] Doing a double step")
            self._rotors[0].step()
            self._rotors[1].step()
            self._double_step = False

        # Only continue if there is more If stepping to be done.
        if not will_step_next_rotor:
            return

        # Move to next rotor.
        rotor_position -= 1
        rotor = self._rotors[rotor_position]

        # Step the next rotor.
        rotor.step()

        # If the 2nd rotor will step rotor 1 (left most one) then a double-step
        # needs to take place.  This is where the middle rotor will step again
        # next button press, along with the left one.
        if rotor.will_step_next():
            self._double_step = True
#endif
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

// # 253 #
