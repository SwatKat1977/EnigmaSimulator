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
import unittest
from simulation.logger import Logger
from simulation.rotor_contact import RotorContact
from simulation.rotor import Rotor

class UnitTest_Rotor(unittest.TestCase):
    ''' Unit tests for the Rotor class '''

    PASS_THROUGH_ROTOR_WIRING = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def setUp(self):
        self._logger = Logger(__name__, write_to_console=False)
        self._valid_pass_through_rotor = Rotor('Pass Through Rotor',
                                               self.PASS_THROUGH_ROTOR_WIRING,
                                               ["Q"],
                                               self._logger)

    def test_validte_property_values(self):
        ''' Validate the rotor properties. '''
        self.assertEqual(self._valid_pass_through_rotor.name, 'Pass Through Rotor')
        self.assertEqual(self._valid_pass_through_rotor.wiring, self.PASS_THROUGH_ROTOR_WIRING)
        self.assertEqual(self._valid_pass_through_rotor.notches, ['Q'])

        self._valid_pass_through_rotor.position = 10
        self.assertEqual(self._valid_pass_through_rotor.position, 10)

        # Test Rotor position setter and getter.
        try:
            self._valid_pass_through_rotor.position = 26

        except ValueError as ex:
            self.assertEqual(str(ex), "Invalid rotor positions")

        else:
            self.fail('ValueError not raised')

        # Test Ring Setting setter and getter.
        self._valid_pass_through_rotor.ring_setting = 10
        self.assertEqual(self._valid_pass_through_rotor.ring_setting, 10)

        try:
            self._valid_pass_through_rotor.ring_setting = 30

        except ValueError as ex:
            self.assertEqual(str(ex), "Invalid ring positions")

        else:
            self.fail('ValueError not raised')

    def test_wiring_not_string(self):
        ''' Test type check for wiring in constructor. '''

        try:
            Rotor('Test rotor', ['self.valid_rotor_wiring'], ["Q"], self._logger)

        except ValueError as ex:
            self.assertEqual(str(ex), "Rotor wiring is not a string")

        else:
            self.fail('ValueError not raised')

    def test_wiring_incorrect_length(self):
        try:
            Rotor('Test rotor', 'ABC', ["Q"], self._logger)

        except ValueError as ex:
            self.assertEqual(str(ex), "Rotor wiring incorrect length")

        else:
            self.fail('ValueError not raised')


    def test_encrypt_forward_simple_at_start(self):
        ''' The most basic of forward encrypts where the rotor is in position A
            and the letter A is pressed. '''

        rotor = Rotor('Test', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ["Q"], self._logger)
        self.assertEqual(rotor.encrypt(RotorContact.A), RotorContact.E)

    def test_encrypt_backwards_simple(self):
        ''' The most basic of backwards encrypts where the rotor is in position
            A and the letter F is pressed. '''

        self.assertEqual(self._valid_pass_through_rotor.encrypt(RotorContact.F,
                                                                forward=False),
                         RotorContact.F)

    def test_will_step_next(self):
        # Test will not step.
        self.assertEqual(self._valid_pass_through_rotor.will_step_next(), False)

        # Test will step.
        self._valid_pass_through_rotor.position = RotorContact.Q.value
        self.assertEqual(self._valid_pass_through_rotor.will_step_next(), True)

    def test_step(self):
        # Simple step test from 1 to 2.
        self.assertEqual(self._valid_pass_through_rotor.position, 1)
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 2)

        self._valid_pass_through_rotor.position = 25
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 1)

    # def encrypt(self, contact : RotorContact, forward = True):
    #     self._logger.log_debug(
    #         f"Encrypting '{contact} on rotor {self._name}, foward = {forward}")
    #     self._logger.log_debug(f"=> Rotor position = {self._position}")

    #     # STEP 1: Correct the input contact entrypoint for position
    #     contact_position = (contact.value + self._position - 1)
    #     self._logger.log_debug("=> Compensating rotor entry. Originally " + \
    #         f"'{contact.name}', now '{RotorContact(contact_position).name}'")
    #     contact_position = contact_position % self.MAX_CONTACT_NO

    #     if forward:
    #         output_contact = RotorContact[self._wiring[contact_position]]
    #         self._logger.log_debug(
    #             f"=> Foward Rotor position = '{output_contact.name}'")

    #     else:
    #         letter = RotorContact(contact_position).name
    #         output_contact = RotorContact(self._wiring.index(letter))
    #         self._logger.log_debug(
    #             f"=> Backwards Rotor position = '{output_contact.name}'")

    #     # STEP 3: Take rotor offset into account
    #     new_position = output_contact.value - (self._position - 1)
    #     self._logger.log_debug("=> Adjusting outgoing rotor, it was " + \
    #         f"'{output_contact.name}'")
    #     output_contact = new_position if new_position else (26 - new_position)
    #     print('new position is:::', new_position, type(new_position))

    #     self._logger.log_debug(
    #         f"=> Outgoing Rotor position = '{RotorContact(output_contact).name}'")
    #     return RotorContact(output_contact)



    # def test_ForwardCircuit_NoOffsetNoRingSetting(self):
    #     # Default position is 1, but make 100% sure do it again!
    #     self._valid_rotor.position = 1

    #     # Verify a couple of different values: Contact 1 ('A')
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.A),
    #                      RotorContact(self._valid_rotor.wiring[RotorContact.A.value]))

    #     # Verify a couple of different values: Contact 13 ('M')
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.N),
    #                      RotorContact(self._valid_rotor.wiring[RotorContact.N.value]))

    #     # Verify a couple of different values: Contact 26 ('Z')
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.Z),
    #                      RotorContact(self._valid_rotor.wiring[RotorContact.Z.value]))


    # ##
    # # Test ForwardCircuit : Initial position not wrapping and no ring setting.
    # # The rotor is in a position other than 1, but it's not enough for the
    # # position to wrap to the beginning of the rotor.  For this test no ring
    # # setting has been set.
    # # @param self The object pointer.
    # def test_ForwardCircuit_NoneStartWrappingOffsetNoRingSetting(self):

    #     # Default position is 1, but make 100% sure do it again!
    #     self._valid_rotor.position = 2

    #     # Verify a couple of different values: Contact 1 ('A')
    #     expected_contact = RotorContact(self._valid_rotor.wiring[1 + (self._valid_rotor.position -1)] -1)
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.A),
    #                      expected_contact)

    #     # Verify a couple of different values: Contact 13 ('M')
    #     expected_contact = RotorContact(self._valid_rotor.wiring[13 + (self._valid_rotor.position -1)] -1)
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.M),
    #                      expected_contact)


    # ##
    # # Test ForwardCircuit : Initial position not wrapping and no ring setting.
    # # The rotor is in a position other than 1, but it's not enough for the
    # # position to wrap to the beginning of the rotor.  For this test no ring
    # # setting has been set.
    # # @param self The object pointer.
    # def test_ForwardCircuit_HasStartWrappingOffsetNoRingSetting(self):

    #     # Default position is 1, but make 100% sure do it again!
    #     # Set position to 20 'T'
    #     self._valid_rotor.position = 20

    #     # Verify that on pressing contact 9 'I' we get the encoded contact of
    #     # 19 'S' out taking into account the position of the rotor.  
    #     # Explanation:
    #     # Contact 9 pressed with position of 20 gives us 28 (-1 as 1 is 'none')
    #     # Since we can't have that position we wrap it around to 2 (28 - 26).
    #     # Contact 2 is wired to 11, but then reversing the position to get back
    #     # to the right contact gives you -8 (again -1 as 1 is 'no postion), 
    #     # which wraps to contact no. of 18.
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.I),
    #                     RotorContact.R)

    #     # Verify that on pressing contact 20 'T' we get the encoded contact of
    #     # 22 'V' out taking into account the position of the rotor.  
    #     # Explanation:
    #     # Contact 20 pressed with position of 20 gives us 39 (-1 as 1 is 'none')
    #     # Since we can't have that position we wrap it around to 13 (39 - 26).
    #     # Contact 13 is wired to 15, but then reversing the position to get back
    #     # to the right contact gives you -4 (again -1 as 1 is 'no postion),
    #     # which wraps to contact no. of 22.
    #     self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.T),
    #                      RotorContact.V)


    # def test_ReturnCircuit_NoOffsetNoRingSetting(self):
    #     # Default position is 1, but make 100% sure do it again!
    #     self._valid_rotor.position = 1

    #     # Verify a couple of different values: Contact 1 ('A')
    #     self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.A),
    #                      RotorContact.U)

    #     # Verify a couple of different values: Contact 13 ('M')
    #     self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.M),
    #                      RotorContact.C)

    #     # Verify a couple of different values: Contact 26 ('Z')
    #     self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.Z),
    #                      RotorContact.J)

    # ##
    # # Test ReturnCircuit : Initial position not wrapping and no ring setting.
    # # The rotor is in a position other than 1, but it's not enough for the
    # # position to wrap to the beginning of the rotor.  For this test no ring
    # # setting has been set.
    # # @param self The object pointer.
    # def test_ReturnCircuit_NoneStartWrappingOffsetNoRingSetting(self):

    #     # Default position is 1, but make 100% sure do it again!
    #     self._valid_rotor.position = 1

    #     # Verify a couple of different values: Contact 1 ('A')
    #     pressed_key = RotorContact.A
    #     contact = pressed_key.value + (self._valid_rotor.position -1)
    #     out_contact = self._valid_rotor.reverse_wiring[contact]
    #     self.assertEqual(self._valid_rotor.get_return_circuit(pressed_key),
    #                      RotorContact(out_contact))

    #     # Verify a couple of different values: Contact 13 ('M')
    #     pressed_key = RotorContact.M
    #     contact = pressed_key.value + (self._valid_rotor.position -1)
    #     out_contact = self._valid_rotor.reverse_wiring[contact]
    #     # (wiring.keys()[wiring.values().index(contact)]
    #     #             - (self._valid_rotor.position -1))
    #     self.assertEqual(self._valid_rotor.get_return_circuit(pressed_key),
    #                      RotorContact(out_contact))


    # ##
    # # Test ReturnCircuit : Initial position not wrapping and no ring setting.
    # # The rotor is in a position other than 1, but it's not enough for the
    # # position to wrap to the beginning of the rotor.  For this test no ring
    # # setting has been set.
    # # @param self The object pointer.
    # def test_ReturnCircuit_HasStartWrappingOffsetNoRingSetting(self):

    #     # Default position is 1, but make 100% sure do it again!
    #     # Set position to 20 'T'
    #     self._valid_rotor.position = RotorContact.T.value

    #     # Verify that on pressing contact 9 'I' we get the encoded contact of
    #     # 4 'D' out taking into account the position of the rotor.
    #     # Explanation:
    #     # Contact 9 pressed with position of 20 gives us 28 (-1 as 1 is 'none')
    #     # Since we can't have that position we wrap it around to 2 (28 - 26).
    #     # Contact 2 is wired to 23, but then reversing the position to get back
    #     # to the right contact gives you -4 (again -1 as 1 is 'no postion).
    #     self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.I), 
    #                      RotorContact.D)

    #     # Verify that on pressing contact 20 'T' we get the encoded contact of
    #     # 10 'J' out taking into account the position of the rotor.
    #     # Explanation:
    #     # Contact 20 pressed with position of 20 gives us 39 (-1 as 1 is 'none')
    #     # Since we can't have that position we wrap it around to 13 (39 - 26).
    #     # Contact 13 is wired to 3, but then reversing the position to get back
    #     # to the right contact gives you -16  (again -1 as 1 is 'no postion),
    #     # which wraps to contact no. of 10.
    #     self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.T),
    #                      RotorContact.J)
    # '''

if __name__ == '__main__':
    unittest.main()
