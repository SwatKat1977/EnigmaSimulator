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
#include "Rotor.h"

namespace enigmaSimualator {

    Rotor::Rotor (std::string rotor_name,
        std::string wiring_name,
        std::vector<RotorContact> notch_locations)
        : rotor_name_ (rotor_name), wiring_name_ (wiring_name),
        notch_locations_ (notch_locations)
    {
    }

    void Rotor::RotorPosition (RotorContact position)
    {
        rotor_position_ = position;
    }

    void Rotor::Step ()
    {
        rotor_position_ = RotorContact((rotor_position_ + 1) % MAX_CONTACT_NO);
    }
 
    void Rotor::Encrypt (RotorContact contact, bool forward)
    {
        /*
        Encrpyting a character is done in three stages:

        === STEP 1 ===
        Correct the input contact entrypoint for position :
        Take into account the current position of the rotor and determine if it
        has wrapped past the letter 'Z'.

        Example 1
        'A' is pressed with the rotor in position 1 ('A'), it will returns the
        output from 'A'. Enigma Rotor 1 will return 'E' for letter 'A'.

        Example 2
        'A' is pressed with the rotor in position 2 ('B'), it will return the
        output from 'B' ('A' has been moved on 1 as rotor is in position 'B').
        Enigma Rotor 1 will return 'K' for a letter 'B'

        === STEP 2 ===
        Take ring settings into account : CURRENTLY NOT IMPLEMENTED

        === STEP 3 ===
        Take rotor offset into account
        When a rotor has stepped, the offset must be taken into account when it
        comes to the output and the entrypoint of the next rotor.
        
        Example 1
        'A' is pressed with the rotor in 'B' (1) position, it will return the
        output from 'B' as rotor is in position 'B', e.g.Enigma Rotor 1 will
        return 'K' for 'B', but as the rotor is in position 'B' (forward 1) the
        exit position is offset by 1 which means 'J' is returned.
        
        Example 2
        'Z' is pressed with the rotor in 'B' (1) position, it will return the
        output from 'A' as rotor is in position 'B' and this then wraps ('Z'
        forward 1 = 'A'), e.g.Enigma Rotor 1 will return 'E' for a letter 'A',
        but the rotor is in position 'B' (forward 1) so 'J' is returned.
        */

        printf ("Encrypting '%d' on rotor %s, foward = %d\n",
            contact, rotor_name_.c_str(), forward);
        printf ("=> Rotor position = %d\n", rotor_position_);

        // STEP 1: Correct the input contact entrypoint for position
        auto contact_position = DetermineNextPosition (contact + rotor_position_);

        printf (
            "=> Compensating rotor entry. Originally '%d', now '%d'",
            contact, contact_position);

        if (forward)
        {
            auto output_contact = RotorContact[_wiring[contact_position]];
            printf ("=> Foward Rotor position = '{output_contact.name}'");
        }
        else
        {
            auto letter = RotorContact (contact_position).name;
            auto output_contact = RotorContact (_wiring.index (letter));
            printf ("=> Backwards Rotor position = '{output_contact.name}'");
        }

        // STEP 2: Take ring settings into account
        // Ring settings are not implemented - untested code
        
#ifdef __USE_UNTESTED_CODE__
        if self.__ringSetting > 1:
            outputPin = outputPin + (self.__ringSetting -1)

        if (outputPin - (self.__ringSetting -1)) <= 0:
            outputPin = NumberOfRotorPins - ((self.__ringSetting - 1) \
            - outputPin)
        else:
            outputPin -= (self.__ringSetting - 1)

        if outputPin > NumberOfRotorPins:
            outputPin = outputPin - NumberOfRotorPins;
            final_contact = output_contact
#endif

        // STEP 3: Take rotor offset into account
        printf ("=> Adjusting outgoing rotor, it was '%d'\n", output_contact);

        output_contact = DetermineNextPosition (output_contact.value -
            rotor_position_);
        printf ("=> Outgoing Rotor position = '%d'", output_contact);
        return RotorContact (output_contact);
    }

#ifdef __OLD_CODE__
    def will_step_next(self) -> bool:
        '''
        Check to see if the rotor will cause the next one to also step.
        @return True if when this steps it will cause the next to to, otherwise
                False is returned.
        '''
        curr_position = RotorContact(self._position).name
        return curr_position in self._notch_locations

    def _determine_next_position(self, contact : int) -> int:

        if contact in [0, 25]:
            new_pos = contact

        elif contact >= 1:
            if contact > self.MAX_CONTACT_NO:
                new_pos = (contact % self.MAX_CONTACT_NO) -1

            else:
                new_pos = contact

        else:
            new_pos = (self.MAX_CONTACT_NO + 1) + contact

        return new_pos
#endif

}   // namespace enigmaSimualator
