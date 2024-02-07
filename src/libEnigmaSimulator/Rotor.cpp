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
#include "Logging.h"

namespace enigmaSimulator {

    const int MAX_CONTACT_NO = 26;

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
            throw std::runtime_error ("Wiring layout is not valid");
        }

        wiring_ = wiring;
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

        DEBUG_LOG ("Rotor::Encrypt() Entering...\n")
        DEBUG_LOG ("=> Contact '%s' (%d) | rotor : '%s' | forward : %d\n",
            RotorContactStr[contact], contact, rotor_name_.c_str(), forward)
        DEBUG_LOG ("=> Current Rotor position : '%s' (%d)\n",
            RotorContactStr[rotor_position_], rotor_position_)

        DEBUG_LOG("=> Offset : %d\n", rotor_position_ - kRotorContact_A)

        // STEP 1: Correct the input contact entrypoint for position
        auto contact_position = OffsetContactPosition (
            contact, rotor_position_ - kRotorContact_A);

        DEBUG_LOG("|==== STEP 1: Correct input contact with rotor position ====|\n")
        DEBUG_LOG (
            "=> Contact after position correction rotor : '%s' (%d) => '%s' (%d)\n",
            RotorContactStr[contact],
            contact,
            RotorContactStr[contact_position],
            contact_position);

        RotorContact output_contact = kRotorContact_end;

        if (forward)
        {
            output_contact = wiring_.GetDestination(contact_position);
            DEBUG_LOG ("=> Forward destination contact for '%s' (%d) : '%s' (%d)\n",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact)
        }
        else
        {
            output_contact = wiring_.GetDestination (contact_position, true);
            DEBUG_LOG ("=> Backwards destination contact for '%s' (%d) : '%s' (%d)\n",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact)
        }

        DEBUG_LOG("|==== STEP 2: Correct input contact with ring position ====|\n")
        // STEP 2: Correct input contact using ring position
        // Ring positions are not implemented - untested code

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

        DEBUG_LOG("|==== STEP 3: Correct input contact with rotor offset ====|\n")

        // STEP 3: Take rotor offset into account
        DEBUG_LOG (
            "=> Adjusting destination rotor for offset : '%s' (%d) by %d\n",
        RotorContactStr[output_contact], output_contact, -rotor_position_)

        output_contact = OffsetContactPosition (
            output_contact, -(rotor_position_ - kRotorContact_A));
        DEBUG_LOG ("=> Outgoing Rotor position = '%s' (%d)\n",
        RotorContactStr[output_contact], output_contact)

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

    RotorContact Rotor::OffsetContactPosition (RotorContact contact,
                                               const int offset)
    {
       DEBUG_LOG ("Rotor::OffsetContactPosition() Entering...\n")
        DEBUG_LOG("=? Offsetting Rotor '%s' (%d) by %d positions\n",
               RotorContactStr[contact], contact, offset)

        int new_position = contact + offset;

        if (new_position > kRotorContact_Z)
        {
            DEBUG_LOG("=> Positive rotor offset\n")
            new_position = (new_position % MAX_CONTACT_NO); // - 1;
        }
        else if (new_position < kRotorContact_A)
        {
            DEBUG_LOG("=> Negative rotor offset\n")
            new_position = MAX_CONTACT_NO + new_position;
        }

        DEBUG_LOG("=> Offsetted rotor is '%s' (%d)\n",
               RotorContactStr[new_position], new_position)

       DEBUG_LOG ("Rotor::OffsetContactPosition() Leaving...\n")
        return RotorContact(new_position);
    }

}   // namespace enigmaSimulator
