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
        RotorWiringLayout wiring,
        std::vector<RotorContact> notches,
        RotorContact initialPosition)
        : rotor_name_ (rotor_name),
          notches_ (notches),
          rotor_position_(initialPosition)
    {
        if (!wiring.IsValid ())
        {
            delete this;
            throw std::runtime_error ("Wiring layout is not valid");
        }
    }

    void Rotor::RotorPosition (RotorContact position)
    {
        rotor_position_ = position;
    }

    void Rotor::Step ()
    {
        rotor_position_ = RotorContact((rotor_position_ + 1) % MAX_CONTACT_NO);
    }

    RotorContact Rotor::Encrypt (RotorContact contact, bool forward)
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
        auto contact_position = DetermineNextPosition (
            RotorContact ((int)(contact)+(int)rotor_position_));

        printf (
            "=> Compensating rotor entry. Originally '%d', now '%d'",
            contact, contact_position);

        RotorContact output_contact = kRotorContact_end;

        if (forward)
        {
            output_contact = wiring_.GetDestination(contact_position);
            printf ("=> Foward Rotor position = '{output_contact.name}'");
        }
        else
        {
            output_contact = wiring_.GetDestination (contact_position, true);
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

        output_contact = DetermineNextPosition (
            RotorContact(output_contact - rotor_position_));
        printf ("=> Outgoing Rotor position = '%d'", output_contact);
        return output_contact;
    }


    /*
        Check to see if this rotor will cause the following also step. It
        returns true if it will cause the next to to, otherwise false.
    */
    bool Rotor::WillStepNext ()
    {
        return std::find (notches_.begin (),
                          notches_.end (), rotor_position_)
                          != notches_.end ();
    }

    RotorContact Rotor::DetermineNextPosition (RotorContact contact)
    {
        return kRotorContact_A;

#ifdef __CODE__
        if (contact in[0, 25])
        {
            new_pos = contact;
        }
        else if (contact >= 1)
        {
            if (contact > MAX_CONTACT_NO)
            {
                new_pos = (contact % MAX_CONTACT_NO) - 1;
            }
            else
            {
                new_pos = contact;
            }
        }
        else
            new_pos = (MAX_CONTACT_NO + 1) + contact;

        return new_pos;
#endif
    }

}   // namespace enigmaSimualator
