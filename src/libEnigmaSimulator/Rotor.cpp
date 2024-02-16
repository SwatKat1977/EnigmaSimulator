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
          ring_position_(kRotorContact_A),
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

        Example 1
        'A' is pressed with 'Rotor I' in position 1 (A), with the ring position
        at position 1 (A) will return the output from 'A' (Rotor I returns 'E').

        Example 2
        'A' is pressed with 'Rotor 1' in position 2 (B), with the ring position
        at position 1 (A) will return the output from 'B' ('A' has been moved
        on 1 due to rotor position 'B'. (Rotor 1 returns 'J' for a letter 'B').

        STEP 1 : Correct the input contact entrypoint for position
        Take into account the current position of the rotor and determine if it
        has wrapped past the letter 'Z'.

        STEP 2 : Correct for ring position : CURRENTLY NOT IMPLEMENTED

        STEP 3 : Get destination for contact

        STEP 4 : Correct the output contact for position
        If the rotor position has moved then the output contact needs to
        corrected back.  E.g. If in position 2 (B) then 'A' will return 'J' as
        it's 'K' offset 1 position.
        */
        DebugLog( "Rotor::" + std::string(__func__), "Rotor '%s'",
            rotor_name_.c_str() );
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Input : '%s' (%d) | forward : %s",
            RotorContactStr[contact], contact, forward ? "Y" : "N");
        DebugLog( "Rotor::" + std::string(__func__),
                  "=> Rotor position : '%s' (%d) | Offset by %d",
            RotorContactStr[rotor_position_], rotor_position_,
            rotor_position_ - kRotorContact_A);

        // STEP 1: Correct the input contact entrypoint for position
        int rotorOffset = rotor_position_ - kRotorContact_A;
        auto contact_position = OffsetContactPosition (
            contact, rotorOffset);
        DebugLog( "Rotor::" + std::string(__func__),
                  "|==== STEP 1: Correct input contact with rotor position ====|");
        DebugLog( "Rotor::" + std::string(__func__),
            "=> Contact after position correction rotor : '%s' (%d) => '%s' (%d)",
            RotorContactStr[contact], contact,
            RotorContactStr[contact_position], contact_position);

        RotorContact output_contact = kRotorContact_end;

        if (forward)
        {
            output_contact = wiring_.GetDestination(contact_position);
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Forward destination contact for '%s' (%d) : '%s' (%d)",
                RotorContactStr[contact_position],
                contact_position,
                RotorContactStr[output_contact],
                output_contact);
        }
        else
        {
            output_contact = wiring_.GetDestination (contact_position, false);
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
#ifdef __UNTESTED__
        if (ring_position_ > kRotorContact_A)
        {
            int ringPosition = ring_position_ - kRotorContact_A;
            output_contact = OffsetContactPosition();
            outputPin = outputPin + (self.__ringSetting -1);
        }

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
        int new_position = contact + offset;

        if (new_position > kRotorContact_Z)
        {
            DebugLog( "Rotor::" + std::string(__func__),
                      "=> Positive rotor offset");
            new_position = (new_position % MAX_CONTACT_NO); // - 1;
        }
        else if (new_position < kRotorContact_A)
        {
            DebugLog( "Rotor::" + std::string(__func__),
                "=> Negative rotor offset");
            new_position = MAX_CONTACT_NO + new_position;
        }

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
            dest += RotorContactStr[wiring_.GetDestination(
                RotorContact(contact))];
            contact++;
        }

        TraceLog( kLogLevel_trace,
                  "Source      : %s", src.c_str());
        TraceLog( kLogLevel_trace,
                  "Destination : %s", dest.c_str());
    }

}   // namespace enigmaSimulator
