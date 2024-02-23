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
        RecalculateWiring ();
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
                  "=> Contact '%c' (%d) | rotor : '%s' | forward : %d",
            RotorContactStr[contact], contact, rotor_name_.c_str(), forward);
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Current Rotor position : '%c' (%d) is offset by %d",
            RotorContactStr[rotor_position_], rotor_position_,
            rotor_position_ - kRotorContact_A);

        // STEP 1: Correct the input contact entrypoint for position
        auto contact_position = OffsetContactPosition (
            contact, rotor_position_ - kRotorContact_A);

        DebugLog( "Rotor::" + std::string(__func__),
                  "|==== STEP 1: Correct input contact with rotor position ====|");
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Contact after position correction rotor : '%c' (%d) => '%c' (%d)",
            RotorContactStr[contact],
            contact,
            RotorContactStr[contact_position],
            contact_position);

        RotorContact output_contact = kRotorContact_end;

        if (forward)
        {
            output_contact = wiring_.WiringPathForward (contact_position);
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Forward destination contact for '%c' (%d) : '%c' (%d)",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact);
        }
        else
        {
            output_contact = wiring_.WiringPathReverse (contact_position);
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Backwards destination contact for '%c' (%d) : '%c' (%d)",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact);
        }

        DebugLog( "Rotor::" + std::string(__func__),
            "|==== STEP 2: Correct input contact with rotor offset ====|");

        // STEP 3: Take rotor offset into account
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Adjusting destination rotor for offset : '%c' (%d) by %d",
        RotorContactStr[output_contact], output_contact, -rotor_position_);

        output_contact = OffsetContactPosition (
            output_contact, -(rotor_position_ - kRotorContact_A));
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Outgoing Rotor position = '%c' (%d)",
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
                  "=> Offsetting Rotor '%c' (%d) by %d positions",
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
                  "=> Offsetted rotor is '%c' (%d)",
               RotorContactStr[new_position], new_position);

        return RotorContact(new_position);
    }

    void Rotor::PrettyPrintWiring()
    {
        TraceLog( kLogLevel_trace,
                  "Source      : %s", wiring_.GetSrcWiringPathStr().c_str());
        TraceLog( kLogLevel_trace,
                  "Destination : %s", wiring_.GetDestWiringPathStr().c_str());
    }

    void Rotor::RecalculateWiring ()
    {
        auto src = wiring_default_.GetSrcWiringPathStr ();
        auto dest = wiring_default_.GetDestWiringPathStr ();

        // Stage 1 : Modify wiring based on ring position.
        if (ring_position_ > kRotorContact_A)
        {
            // 1] Get the offset ring (remove 1 to account for position 'a').
            int ring_offset = static_cast<int>(ring_position_)
                - static_cast<int>(kRotorContact_A);
            // 2] Rotate all destination wiring 'ring_offset' places right.
            RightRotateString (dest, ring_offset);
            // 3] Offset/increment all destination wiring by 'ring_offset'.
            //    E.g. with ring_offset of 2, 'A' would become 'C'.
            OffsetStringValue (dest, ring_offset);
        }

        // Stage 2 : Modify wiring based on rotor position.
        // 1] Get the rotor offset (remove 1 to account for position 'a').
        int rotor_offset = static_cast<int>(rotor_position_)
            - static_cast<int>(kRotorContact_A);
        // 2] Rotate all source wiring 'rotor_position_' places left.
        LeftRotateString(src, rotor_offset);
        // 2] Rotate all destination wiring 'rotor_position_' places left.
        LeftRotateString(dest, rotor_offset);

        wiring_ = RotorWireConfiguration(dest, src);
    }

}   // namespace enigmaSimulator
