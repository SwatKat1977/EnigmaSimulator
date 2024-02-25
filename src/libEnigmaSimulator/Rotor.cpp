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
        RecalculateWiring ();
    }

    /*
    Encrypt a character forward.

    Example 1
    'A' is pressed with the rotor in position 1 ('A'), it will returns the
    output from 'A'. Enigma Rotor 1 will return 'E' for letter 'A'.

    Example 2
    'A' is pressed with the rotor in position 2 ('B'), it will return the
    output from 'B' ('A' has been moved on 1 as rotor is in position 'B').
    Enigma Rotor 1 will return 'K' for a letter 'B'
    */
    RotorContact Rotor::EncryptForward (RotorContact contact)
    {
        int rotor_offset = rotor_position_ - kRotorContact_A;
        DebugLog( "Rotor::EncryptForward", "=> [%s] Input Contact '%c' (%d)",
             rotor_name_.c_str(), RotorContactStr[contact], contact);
        DebugLog( "Rotor::EncryptForward",
                  "=> Current Rotor position : '%c' (%d) (offset : %d)",
            RotorContactStr[rotor_position_], rotor_position_, rotor_offset);

        auto contact_position = contact;

        RotorContact output_contact = kRotorContact_end;

        output_contact = wiring_.WiringPathForward (contact_position);
        DebugLog( "Rotor::EncryptForward", "=> Destination : '%c' (%d)",
            RotorContactStr[output_contact], output_contact);

        rotor_offset = -(rotor_position_ - kRotorContact_A);
        DebugLog( "Rotor::EncryptForward",
            "=> Adjusting destination rotor for offset : '%c' (%d) by %d",
        RotorContactStr[output_contact], output_contact, rotor_offset);

        output_contact = OffsetContactPosition (
            output_contact, -(rotor_position_ - kRotorContact_A));
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Outgoing Rotor position = '%c' (%d)",
        RotorContactStr[output_contact], output_contact);

        return output_contact;
    }

    /*
    Encrypt a character in reverse.

    Example 1
    'A' is pressed with the rotor in position 1 ('A'), it will returns the
    output from 'A'. Enigma Rotor 1 will return 'E' for letter 'A'.

    Example 2
    'A' is pressed with the rotor in position 2 ('B'), it will return the
    output from 'B' ('A' has been moved on 1 as rotor is in position 'B').
    Enigma Rotor 1 will return 'K' for a letter 'B'
    */
    RotorContact Rotor::EncryptReverse (RotorContact contact)
    {
        int rotor_offset = rotor_position_ - kRotorContact_A;
        DebugLog( "Rotor::EncryptReverse",
                  "=> Contact '%c' (%d) | rotor : '%s'",
            RotorContactStr[contact], contact, rotor_name_.c_str());
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Current Rotor position : '%c' (%d) is offset by %d",
            RotorContactStr[rotor_position_], rotor_position_, rotor_offset);

        // Correct the input contact entrypoint for position
        auto contact_position = OffsetContactPosition (
            contact, rotor_position_ - kRotorContact_A);

        RotorContact output_contact = kRotorContact_end;

        // Get the destination, in this case the 'source'.
        output_contact = wiring_.WiringPathReverse (contact_position);
        DebugLog( "Rotor::EncryptReverse",
            "=> Backwards destination contact for '%c' (%d) : '%c' (%d)",
            RotorContactStr[contact_position],
            contact_position,
            RotorContactStr[output_contact],
            output_contact);

        DebugLog( "Rotor::EncryptReverse",
            "=> Adjusting destination rotor for offset : '%c' (%d) by %d",
        RotorContactStr[output_contact], output_contact, -rotor_position_);

        output_contact = OffsetContactPosition (
            output_contact, -(rotor_position_ - kRotorContact_A));
        DebugLog( "Rotor::EncryptReverse",
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
