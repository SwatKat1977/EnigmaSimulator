'''
    EnigmaSimulator - A software implementation of the Engima Machine.
    Copyright (C) 2015-2020 Engima Simulator Development Team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''
from rotor_contact import NO_OF_ROTOR_CONTACTS, RotorContact


# ***********************************************************************
# Class representing an Enigma rotor / wheel /drum / Walzen (German).
# ***********************************************************************
class Rotor:
    __slots__ = ['notch_locations', 'reverse_rotor_wiring', 'rotor_name',
                 'rotor_position', 'rotor_ring_setting', 'rotor_wiring']


    ##
    # Property getter : Name of the rotor.
    @property
    def name(self):
        return self.rotor_name

    ##
    # Property getter : How the rotor is wired.
    @property
    def wiring(self):
        return self.rotor_wiring

    ##
    # Property getter 'NotchLocations' : Location of the turnover notch(es).
    @property
    def notches(self):
        return self.notch_locations

    ##
    # Property getter : Position of the rotor.
    @property
    def position(self):
        return self.rotor_position

    @position.setter
    def position(self, value):
        # Validate rotor positions.
        if value < 1 or value > NO_OF_ROTOR_CONTACTS:
            raise ValueError("Invalid rotor positions")

        # Set the position.
        self.rotor_position = value

    ##
    # Property getter 'RingSetting' : Ring setting of the rotor.
    @property
    def ring_setting(self):
        return self.rotor_ring_setting

    @ring_setting.setter
    def ring_setting(self, value):
        if value < 1 or value > NO_OF_ROTOR_CONTACTS:
            raise ValueError("Invalid ring positions")

        self.rotor_ring_setting = value


    ## Rotor constructor method, we wire a rotor from right => left.d.
    # @param self The object pointer.
    # @param name Human readable rotor name.
    # @param wiring Wiring setting from right to left.
    # @param notchLocations Location of the turnover notches.
    def __init__(self, name, wiring, notchLocations):
        # Name of the rotor (e.g. Rotor I).
        self.rotor_name = name

        # Location of the turnover notch(es).
        self.notch_locations = notchLocations

        # Current position of the rotor.
        self.rotor_position = 1

        # Ring setting (Ringstellung) for the rotor
        self.rotor_ring_setting = 1

        # Check to make sure wiring is a list.
        if not isinstance(wiring, (dict)):
            raise ValueError("Incompatible rotor wiring diagram")

        if len(wiring) != NO_OF_ROTOR_CONTACTS:
            raise ValueError("Incomplete wiring diagram")

        # define how the rotor is internally wired.
        self.rotor_wiring = wiring

        self.reverse_rotor_wiring = {v:k for k,v in wiring.items()} 


    ##
    # Step the rotor.
    # @param self The object pointer.
    def step(self):
        if self.rotor_position == NO_OF_ROTOR_CONTACTS:
            self.rotor_position = 1
        else:
            self.rotor_position += 1


    ## Get the output (circuit) using the contacts on the right-hand side
    #  contacts (forward) of the rotor.
    #  @param self The object pointer.
    #  @param contact Reference contact to get circuit with.
    #  @return A contact number.
    def get_forward_circuit(self, contact):

        contact_no = contact.value

        # ===========================================================
        # STEP 1 : Determine the starting point for the input contact
        # ===========================================================
        # This needs to be adjusted for the current position of the rotor.  If
        # the key pressed plus position is greater then NO_OF_ROTOR_CONTACTS
        # then we start at the beginning of the alphabet again.
        # Example 1: 'A' is pressed with position of 'A' will return you the
        #            output from 'A', e.g. for Enigma Rotor 1 will return 'E'
        #            for a letter 'A'.
        # Example 2: 'A' is pressed with position of 'B' will return you the
        #            output from 'B' ('A' has been moved on 1 as now rotor is
        #            in position 'B'), e.g. for Enigma Rotor 1 will return 'K'
        #            for a letter 'B'
        input_contact = (contact_no + self.rotor_position)  -1
        if input_contact > NO_OF_ROTOR_CONTACTS:
            input_contact = input_contact - NO_OF_ROTOR_CONTACTS

        output_contact = self.rotor_wiring[input_contact]

        # ===========================================================
        # STEP 2 : Take ring settings into account
        # ===========================================================
        # CURRENTLY NOT IMPLEMENTED

        # Ring settings are not implemented - untested code
        # if self.__ringSetting > 1:
        #     #outputPin = outputPin + (self.__ringSetting -1)
        #
        #     if (outputPin - (self.__ringSetting -1)) <= 0:
        #         outputPin = NumberOfRotorPins - ((self.__ringSetting -1) \
        #          - outputPin)
        #     else:
        #         outputPin -= (self.__ringSetting -1)
        #
        #     #if outputPin > NumberOfRotorPins:
        #     #    outputPin = outputPin - NumberOfRotorPins;

        final_contact = output_contact

        # ===========================================================
        # STEP 3 : Take rotor offset into account
        # ===========================================================
        # When a rotor has stepped, the offset must be taken into account to
        # know what the output is, and where it enters the next rotor.  If
        # the key pressed plus position is greater then NO_OF_ROTOR_CONTACTS
        # then we start at the beginning of the alphabet again.
        # Example 2: 'A' is pressed with position of 'B' will return you the
        #            output from 'B' as  rotor is in position 'B', e.g. Enigma
        #            Rotor 1 will return 'K' for a letter 'B', but the rotor
        #            is in position 'B' (forward 1) so exit is off by 1, the
        #            output needs to account for this so 'J' is returned.
        # Example 2: 'Z' is pressed with position of 'B' will return you the
        #            output from 'A' as rotor is in position 'B' and this then
        #            wraps about ('Z' forward 1 = 'A'), e.g. Enigma Rotor 1
        #            will return 'E' for a letter 'A', but the rotor is in
        #            position 'B' (forward 1) so exit is off by 1, the output
        #            needs to account for this so 'J' is returned.
        if self.rotor_position > 1:
            if (output_contact - (self.rotor_position -1)) <= 0:
                final_contact = NO_OF_ROTOR_CONTACTS \
                    - ((self.rotor_position -1) - output_contact)

            else:
                final_contact -= (self.rotor_position -1)

        print(f'Final contact: {RotorContact(final_contact)}')
        return final_contact


    ##
    # Get the output (circuit) from the return route using the contacts as a
    # reference.
    # @param self The object pointer.
    # @param contact Reference contact to get circuit with.
    # @return The contact number.
    def get_return_circuit(self, contact):

        contact_no = contact.value
        print(f"::get_return_circuit() Contact : {RotorContact(contact).name}")

        # ===========================================================
        # STEP 1 : Determine the starting point for the input contact
        # ===========================================================
        # This needs to be adjusted for the current position of the rotor.  If
        # the key pressed plus position is greater then NO_OF_ROTOR_CONTACTS
        # then we start at the beginning of the alphabet again.
        # Example 1: 'A' is pressed with position of 'A' will return you the
        #            output from 'A', e.g. for Enigma Rotor 1 will return 'E'
        #            for a letter 'A'.
        # Example 2: 'A' is pressed with position of 'B' will return you the
        #            output from 'B' ('A' has been moved on 1 as now rotor is
        #            in position 'B'), e.g. for Enigma Rotor 1 will return 'K'
        #            for a letter 'B'
        input_contact = contact_no + (self.rotor_position -1)
        if input_contact > NO_OF_ROTOR_CONTACTS:
            input_contact = input_contact - NO_OF_ROTOR_CONTACTS

        # Get the outgoing contact number using the reverse wiriting dictionary.
        output_contact = self.reverse_rotor_wiring[input_contact]
        print(f"::get_return_circuit() output_contact : {RotorContact(output_contact).name}")

        # ===========================================================
        # STEP 2 : Take ring settings into account
        # ===========================================================
        # CURRENTLY NOT IMPLEMENTED

        # if self.__ringSetting > 0:
        #     if (outputPin - (self.__ringSetting -1)) <= 0:
        #         outputPin = NumberOfRotorPins - ((self.__ringSetting -1) \
        #          - outputPin)
        #     else:
        #         outputPin -= (self.__ringSetting -1)
        #
        # Ring settings are not implemented - untested code
        # if self.__ringSetting > 1:
        #     op = outputPin
        #     outputPin = outputPin + (self.__ringSetting -1)
        #     print("[DEBUG] Pin after ring offset : '{0}' [{1}] returns '{2}' [{3}]"
        #     .format(RotorContacts[outputPin], outputPin,
        #      RotorContacts[outputPin], outputPin))
        #
        #     print("[DEBUG] OutputPin = pin ({0}) + ring ({1}) -1 == {2}"
        #     .format(op, self.__ringSetting, outputPin))
        #
        #     if outputPin > NumberOfRotorPins:
        #         outputPin = outputPin - NumberOfRotorPins;

        final_contact = output_contact

        # ===========================================================
        # STEP 3 : Take rotor offset into account
        # ===========================================================
        # When a rotor has stepped, the offset must be taken into account to
        # know what the output is, and where it enters the next rotor.  If
        # the key pressed plus position is greater then NO_OF_ROTOR_CONTACTS
        # then we start at the beginning of the alphabet again.
        # Example 2: 'A' is pressed with position of 'B' will return you the
        #            output from 'B' as  rotor is in position 'B', e.g. Enigma
        #            Rotor 1 will return 'K' for a letter 'B', but the rotor
        #            is in position 'B' (forward 1) so exit is off by 1, the
        #            output needs to account for this so 'J' is returned.
        # Example 2: 'Z' is pressed with position of 'B' will return you the
        #            output from 'A' as rotor is in position 'B' and this then
        #            wraps about ('Z' forward 1 = 'A'), e.g. Enigma Rotor 1
        #            will return 'E' for a letter 'A', but the rotor is in
        #            position 'B' (forward 1) so exit is off by 1, the output
        #            needs to account for this so 'J' is returned.
        if self.rotor_position > 1:
            if (output_contact - (self.rotor_position -1)) <= 0:
                final_contact = NO_OF_ROTOR_CONTACTS \
                    - ((self.rotor_position -1) - output_contact)

            else:
                final_contact -= (self.rotor_position -1)

        print(f'Final contact: {RotorContact(final_contact)}')
        return final_contact


    ##
    # Check to see if the rotor will cause the next one to also step.
    # @param self The object pointer.
    # @return True if when this steps it will cause the next to to, otherwise
    # False is returned.
    def will_step_next(self):
        return self.rotor_position in self.notch_locations
