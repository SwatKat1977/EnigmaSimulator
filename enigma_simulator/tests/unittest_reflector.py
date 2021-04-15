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
import unittest
from simulation.reflector import Reflector
from simulation.rotor_contact import RotorContact

class UnitTestReflector(unittest.TestCase):
    ''' Unit tests for the Reflector class '''

    def test_wiring_string_too_small(self):
        '''
        Test Reflector construction where the wiring string is too small. The
        constructor should raise a ValueError exception with the message of
        'Reflector wiring string incorrect'.
        '''
        with self.assertRaises(ValueError) as context:
            Reflector('wiring_string_too_small', 'ABCDE')

        if 'Reflector wiring string incorrect' not in str(context.exception):
            self.fail("Did not detect 'Reflector wiring string incorrect'")

    def test_wiring_not_a_string(self):
        '''
        # Test Reflector construction where the wiring string is not a string.
        # The constructor should raise the exception 'Incompatible reflector
        # wiring diagram'.
        '''
        with self.assertRaises(ValueError) as context:
            Reflector('wiring_not_a_string', 12345)

        if 'Reflector wiring should be a string' not in str(context.exception):
            self.fail("Did not detect 'Reflector wiring should be a string'")

    def test_construction_success(self):
        ''' Test constructor was successful.  '''
        wiring = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        reflector_name = 'successful'

        reflector = Reflector(reflector_name, wiring)
        self.assertIsNot(reflector, None)
        self.assertEqual(reflector.name, reflector_name)
        self.assertEqual(reflector.wiring, wiring)

    def test_encrypt(self):
        ''' Test constructor was successful.  '''
        test_pin = RotorContact.A
        expected_out_pin = RotorContact.Z

        reflector = Reflector('successful', 'ZYXWVUTSRQPONMLKJIHGFEDCBA')
        self.assertEqual(reflector.encrypt(test_pin), expected_out_pin)

if __name__ == '__main__':
    unittest.main()
