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

    def test_validate_property_values(self):
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

    def test_encrypt_forward_no_offset_or_ring_setting_nowrap(self):
        ''' The most basic of forward encrypts where the rotor is in position A
            and the letter A is pressed. '''

        rotor = Rotor('Test', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ["Q"], self._logger)
        self.assertEqual(rotor.encrypt(RotorContact.A), RotorContact.E)
        self.assertEqual(rotor.encrypt(RotorContact.L), RotorContact.T)
        self.assertEqual(rotor.encrypt(RotorContact.T), RotorContact.P)
        self.assertEqual(rotor.encrypt(RotorContact.Y), RotorContact.C)
        self.assertEqual(rotor.encrypt(RotorContact.Z), RotorContact.J)

    def test_encrypt_forward_offset_no_ring_setting_nowrap(self):
        ''' The most basic of forward encrypts where the rotor is in position A
            and the letter A is pressed. '''

        rotor = Rotor('Test', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ["Q"], self._logger)
        rotor.position = RotorContact.C.value
        self.assertEqual(rotor.encrypt(RotorContact.A), RotorContact.K)

    def test_encrypt_forward_offset_no_ring_setting_wrap(self):
        '''
        Verify that when key 'S' (18) is pressed when the rotor is rotated 3
        positions we get the encoded contact of 'X' (23).

        Explanation:

        Key 'S' (18) is pressed, as the rotor is in position 3 (C) this means
        it goes the wiring circuit of 'U' resulting in an encoded value of 'A'.
        As the rotor is in position 3 we need to adjust the output by a value
        of 2, therefore 'Y' is returned.
        '''
        rotor = Rotor('Test', 'EKMFLGDQVZNTOWYHXUSPAIBRCJ', ["Q"], self._logger)
        rotor.position = RotorContact.C.value
        self.assertEqual(rotor.encrypt(RotorContact.S), RotorContact.Y)

    def test_encrypt_backwards_no_offset_or_ring_setting_nowrap(self):
        '''
        The rotor is in a position other than 1, but it is not enough for the
        position to wrap to the beginning of the rotor. For this test no ring
        setting has been set.
        '''

        self.assertEqual(self._valid_pass_through_rotor.encrypt(RotorContact.F,
                                                                forward=False),
                         RotorContact.F)

    def test_encrypt_backwards_with_offset_no_ring_setting_nowrap(self):
        '''
        Verify that on pressing 'I' (9) we get the encoded value of 'S' (18).

        Explanation:
        'I' (9) is pressed with a rotor position of 3, the encoded letter that
        is returned is 'S' (18) because the input is advanced 2 to 'K', which
        will return the letter 'U'.  Because off the 2 position offset we then
        need to adjust the result down 2 to return 'S'.
        '''

        rotor = Rotor('Test', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ["Q"], self._logger)
        rotor.position = RotorContact.C.value
        self.assertEqual(rotor.encrypt(RotorContact.I, forward=False),
                         RotorContact.S)

    def test_encrypt_backwards_with_offset_no_ring_setting_wrap(self):
        '''
        Verify that on pressing 'Z' (25) we get the encoded value of 'X' (23).

        Explanation:
        'Z' (25) is pressed with a rotor position of 5. The original input is
        advanced 4 to 'D' which will return the letter 'B'.  Because of the
        position offset the result is adjusted down 4 to return 'X'.
        '''
        rotor = Rotor('Test', 'BDFHJLCPRTXVZNYEIWGAKMUSQO', ["Q"], self._logger)
        rotor.position = RotorContact.E.value
        self.assertEqual(rotor.encrypt(RotorContact.Z, forward=False),
                         RotorContact.X)

    def test_will_step_next(self):
        # Test will not step.
        self.assertEqual(self._valid_pass_through_rotor.will_step_next(), False)

        # Test will step.
        self._valid_pass_through_rotor.position = RotorContact.Q.value
        self.assertEqual(self._valid_pass_through_rotor.will_step_next(), True)

    def test_step(self):
        # Simple step test from positioh 1 to 2.
        self.assertEqual(self._valid_pass_through_rotor.position, 0)
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 1)

        # Step test from position 25 (Z) to 1 (A).
        self._valid_pass_through_rotor.position = 25
        self._valid_pass_through_rotor.step()
        self.assertEqual(self._valid_pass_through_rotor.position, 1)

if __name__ == '__main__':
    unittest.main()
