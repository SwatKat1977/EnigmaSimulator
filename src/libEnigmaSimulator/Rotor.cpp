'''
    EnigmaSimulator - A software implementation of the Engima Machine.
    Copyright (C) 2015-2021 Engima Simulator Development Team

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''
from simulation.rotor_contact import RotorContact

class Rotor:
    ''' Class representing an Enigma rotor wheel / drum / Walzen (German). '''
    __slots__ = ['_logger', '_notch_locations', '_name',  '_position',
                 '_ring_setting', '_wiring']

    MAX_CONTACT_NO = 25
    WIRING_LENGTH = 26

    @property
    def name(self) -> str:
        """ Property getter : Name of the rotor. """
        return self._name

    @property
    def wiring(self):
        """ Property getter : How the rotor is wired forwards. """
        return self._wiring

    @property
    def notches(self):
        ''' Property getter 'NotchLocations' : Location of the turnover
            notch or notches. '''
        return self._notch_locations

    @property
    def position(self) -> int:
        ''' Property getter : Position of the rotor. '''
        return self._position

    @position.setter
    def position(self, value):
        ''' Property setter : Position of the rotor. '''

        # Validate rotor positions.
        if value >= 0 and value <= self.MAX_CONTACT_NO:
            self._position = value
            return

        raise ValueError("Invalid rotor positions")

    @property
    def ring_setting(self):
        ''' Property getter 'RingSetting' : Ring setting of the rotor. '''
        return self._ring_setting

    @ring_setting.setter
    def ring_setting(self, value) -> None:
        ''' Property setter 'RingSetting' : Ring setting of the rotor. '''

        if value < 1 or value > self.MAX_CONTACT_NO:
            raise ValueError("Invalid ring positions")

        self._ring_setting = value

    def __init__(self, name : str, wiring : str, notch_locations : list,
                 logger):
        '''
        Rotor constructor method, a rotor is wired from right to left.
        # @param name Human readable rotor name.
        # @param wiring Wiring setting from right to left.
        # @param notch_locations Location of the turnover notches.
        '''

        # Name of the rotor (e.g. Rotor I).
        self._name = name

        # Location of the turnover notch/notches.
        self._notch_locations = notch_locations

        # Current position of the rotor.
        self._position = 0

        # Ring setting (Ringstellung) for the rotor
        self._ring_setting = 0

        self._logger = logger

        if not isinstance(wiring, (str)):
            raise ValueError("Rotor wiring is not a string")

        if len(wiring) != self.WIRING_LENGTH:
            raise ValueError("Rotor wiring incorrect length")

        # define how the rotor is internally wired.
        self._wiring = wiring

    def step(self):
        ''' Step the rotor. '''
        self._position = (self._position + 1) % self.MAX_CONTACT_NO

    def encrypt(self, contact : RotorContact, forward = True):
        '''
        STEP 1: Correct the input contact entrypoint for position:
        Take into account the current position of the rotor and determine if it
        has wrapped past the letter 'Z' (contact number 26).
        Example 1
        'A' is pressed with the rotor in position 1 ('A'), it will returns the
        output from 'A'. E.g. Enigma Rotor 1 will return 'E' for letter 'A'.
        Example 2
        'A' is pressed with the rotor in position 2 ('B'), it will return the
        output from 'B' ('A' has been moved on 1 as rotor is in position 'B').
        E.g. Enigma Rotor 1 will return 'K' for a letter 'B'

        STEP 2: Take ring settings into account:
        CURRENTLY NOT IMPLEMENTED

        STEP 3: Take rotor offset into account
        When a rotor has stepped, the offset must be taken into account when it
        comes to the output and the entrypoint of the next rotor.
        Example 1
        'A' is pressed with the rotor in 'B' (1) position, it will return the
        output from 'B' as rotor is in position 'B', e.g. Enigma Rotor 1 will
        return 'K' for 'B', but as the rotor is in position 'B' (forward 1) the
        exit position is offset by 1 which means 'J' is returned.
        Example 2
        'Z' is pressed with the rotor in 'B' (1) position, it will return the
        output from 'A' as rotor is in position 'B' and this then wraps ('Z'
        forward 1 = 'A'), e.g. Enigma Rotor 1 will return 'E' for a letter 'A',
        but the rotor is in position 'B' (forward 1) so 'J' is returned.

        @param contact Reference contact to get circuit with.
        @return A contact number.
        '''

        self._logger.log_debug(
            f"Encrypting '{contact} on rotor {self._name}, foward = {forward}")
        self._logger.log_debug(f"=> Rotor position = {self._position}")

        # STEP 1: Correct the input contact entrypoint for position
        contact_position = self._determine_next_position(contact.value +
                                                         self._position)
        self._logger.log_debug("=> Compensating rotor entry. Originally " + \
            f"'{contact.name}', now '{RotorContact(contact_position).name}'")

        if forward:
            output_contact = RotorContact[self._wiring[contact_position]]
            self._logger.log_debug(
                f"=> Foward Rotor position = '{output_contact.name}'")

        else:
            letter = RotorContact(contact_position).name
            output_contact = RotorContact(self._wiring.index(letter))
            self._logger.log_debug(
                f"=> Backwards Rotor position = '{output_contact.name}'")

        # STEP 2: Take ring settings into account
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
        # final_contact = output_contact

        # STEP 3: Take rotor offset into account
        self._logger.log_debug("=> Adjusting outgoing rotor, it was " + \
            f"'{output_contact.name}'")

        output_contact = self._determine_next_position(output_contact.value -
                                                       self._position)
        self._logger.log_debug(
            f"=> Outgoing Rotor position = '{RotorContact(output_contact).name}'")
        return RotorContact(output_contact)

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
