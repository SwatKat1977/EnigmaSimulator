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
#include "StringUtils.h"

namespace enigmaSimulator {

    const int MAX_CONTACT_NO = 26;

    Rotor::Rotor (std::string rotor_name,
        RotorWireConfiguration wiring,
        std::vector<RotorContact> notches,
        RotorContact initialPosition)
        : rotor_name_ (rotor_name),
          notches_ (notches),
          ring_position_(kRotorContact_A),
          rotor_position_(initialPosition)
    {
        if (!wiring.HasValidWiring ())
        {
            throw std::runtime_error ("Wiring layout is not valid");
        }

        wiring_ = wiring;
        wiring_default_ = wiring;
    }

    void Rotor::RotorPosition (RotorContact position)
    {
        rotor_position_ = position;
    }

    // Property getter : Position of the ring.
    void Rotor::RingPosition (RotorContact pos)
    {
        ring_position_ = pos;
        RecalculateWiring ();
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

        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Contact '%s' (%d) | rotor : '%s' | forward : %d",
            RotorContactStr[contact], contact, rotor_name_.c_str(), forward);
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Current Rotor position : '%s' (%d) is offset by %d",
            RotorContactStr[rotor_position_], rotor_position_,
            rotor_position_ - kRotorContact_A);

        // STEP 1: Correct the input contact entrypoint for position
        auto contact_position = OffsetContactPosition (
            contact, rotor_position_ - kRotorContact_A);

        DebugLog( "Rotor::" + std::string(__func__),
                  "|==== STEP 1: Correct input contact with rotor position ====|");
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Contact after position correction rotor : '%s' (%d) => '%s' (%d)",
            RotorContactStr[contact],
            contact,
            RotorContactStr[contact_position],
            contact_position);

        RotorContact output_contact = kRotorContact_end;

        if (forward)
        {
            output_contact = wiring_.WiringPathForward (contact_position);
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Forward destination contact for '%s' (%d) : '%s' (%d)",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact);
        }
        else
        {
            output_contact = wiring_.WiringPathReverse (contact_position);
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Backwards destination contact for '%s' (%d) : '%s' (%d)",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact);
        }

        DebugLog( "Rotor::" + std::string(__func__),
            "|==== STEP 2: Correct input contact with ring position ====|");
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

        DebugLog( "Rotor::" + std::string(__func__),
            "|==== STEP 3: Correct input contact with rotor offset ====|");

        // STEP 3: Take rotor offset into account
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Adjusting destination rotor for offset : '%s' (%d) by %d",
        RotorContactStr[output_contact], output_contact, -rotor_position_);

        output_contact = OffsetContactPosition (
            output_contact, -(rotor_position_ - kRotorContact_A));
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Outgoing Rotor position = '%s' (%d)",
        RotorContactStr[output_contact], output_contact);

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
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Offsetting Rotor '%s' (%d) by %d positions",
               RotorContactStr[contact], contact, offset);

        int new_position = contact + offset;

        if (new_position > kRotorContact_Z)
        {
            DebugLog( "Rotor::" + std::string(__func__),
                      "=> Positive rotor offset");
            new_position = (new_position % MAX_CONTACT_NO);
        }
        else if (new_position < kRotorContact_A)
        {
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Negative rotor offset");
            new_position = MAX_CONTACT_NO + new_position;
        }

        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Offsetted rotor is '%s' (%d)",
               RotorContactStr[new_position], new_position);

        return RotorContact(new_position);
    }

    void Rotor::PrettyPrintWiring()
    {
        int contact = kRotorContact_A;
        std::string src;
        std::string dest;

        while (contact <= kRotorContact_Z)
        {
            src += RotorContactStr[contact];
            dest += RotorContactStr[wiring_.WiringPathForward (
                RotorContact(contact))];
            contact++;
        }

        TraceLog( kLogLevel_trace,
                  "Source      : %s", src.c_str());
        TraceLog( kLogLevel_trace,
                  "Destination : %s", dest.c_str());
    }

    void Rotor::RecalculateWiring ()
    {
        auto src = wiring_default_.GetSrcWiringPathStr ();
        auto dest = wiring_default_.GetDestWiringPathStr ();

        if (ring_position_ > kRotorContact_A)
        {
            int ring_offset = static_cast<int>(ring_position_)
                - static_cast<int>(kRotorContact_A);
            RightRotateString (dest, ring_offset);
            OffsetStringValue (dest, 1);
        }

        wiring_ = RotorWireConfiguration(dest, src);
    }

    // abcdefghijklmnopQrstuvwxyz
    // ekmflgdqvzntowyhxuspaibrcj

    // abcdefghijklmnopQrstuvwxyz
    // kflngmherwaoupxziyvtqbjcsd

}   // namespace enigmaSimulator
