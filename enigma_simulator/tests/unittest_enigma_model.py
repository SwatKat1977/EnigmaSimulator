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
from simulation.enigma_model import EnigmaModel, RotorCount

class UnitTestEnigmaModel(unittest.TestCase):
    ''' Unit tests for the Enigma Model class. '''

    def test_verify_getters(self):
        ''' EnigmaModel : Test getters '''

        rotors = ["Rotor I", "Rotor II", "Rotor III"]
        reflectors = ['wide_a']
        setup = EnigmaModel('Test Enigma 1', 'Enigma1', RotorCount.THREE, True, rotors, reflectors)

        self.assertEqual(setup.short_name, 'Enigma1')
        self.assertEqual(setup.long_name, 'Test Enigma 1')
        self.assertEqual(setup.no_of_rotors, RotorCount.THREE)
        self.assertEqual(setup.rotors, rotors)
        self.assertEqual(setup.has_plugboard, True)
        self.assertEqual(setup.reflectors, reflectors)

    def test_invalid_number_of_rotors(self):
        ''' EnigmaModel : Test Invalid number of rotors '''

        rotors = ["Rotor I", "Rotor II", "Rotor III"]
        reflectors = ['wide_a']

        try:
            EnigmaModel('Test Enigma 1', 'Enigma1', 3, True, rotors, reflectors)
            self.fail("ValueError exception Invalid number of rotors not raised")

        except ValueError as excpt:
            expected = 'Invalid number of rotors'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
                self.fail(err_msg)

if __name__ == '__main__':
    unittest.main()
