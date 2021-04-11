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


# ******************************
# Unit tests for the Rotor class
# ******************************
class UnitTest_Reflector(unittest.TestCase):

    ValidWiring = \
    {
        1 : 25,
        2 : 18,
        3 : 21,
        4 : 8,
        5 : 17,
        6 : 19,
        7 : 12,
        8 : 4,
        9 : 16,
        10 : 24,
        11 : 14,
        12 : 7,
        13 : 15,
        14 : 11,
        15 : 13,
        16 : 9,
        17 : 5,
        18 : 2,
        19 : 6,
        20 : 26,
        21 : 3,
        22 : 23,
        23 : 22,
        24 : 10,
        25 : 1,
        26 : 20,
    }


    ##
    # Test Constructor : Wiring matrix too small.
    # The constructor should raise the exception 'Incomplete reflector wiring
    # diagram'  when the wiring matrix is too small (not 26 contacts).
    # @param self The object pointer.
    def test_Constructor_WiringTooSmall(self):

        wiring = {1 : 25, 2 : 18}

        # Attempt to create a reflector, it should raise a ValueError
        # exception.
        with self.assertRaises(ValueError) as context:
            reflector = Reflector('WiringTooSmall', wiring)

        # Verify that the the exception was caught.
        if 'Incomplete reflector wiring diagram' not in str(context.exception):
            self.fail("Did not detect 'Incomplete reflector wiring diagram'")


    ##
    # Test Constructor : Wiring matrix is not a dictionary.
    # The constructor should raise the exception 'Incompatible reflector
    # wiring diagram'.
    # @param self The object pointer.
    def test_Constructor_WiringNotDictionary(self):

        wiring = "{ 1 : 25, 2 : 18 }"

        # Attempt to create a reflector, it should raise a ValueError
        # exception.
        with self.assertRaises(ValueError) as context:
            reflector = Reflector('WiringNotDictionary', wiring)
        
        # Verify that the the exception was caught.
        if 'Incompatible reflector wiring diagram' not in str(context.exception):
            self.fail("Did not detect 'Incompatible reflector wiring diagram'")


    ## Test Constructor : OK. The constructor was successful.
    #  @param self The object pointer.
    def test_Constructor_OK(self):
        test_pin = RotorContact.A
        expected_out_pin = RotorContact.Y

        reflector = Reflector('OK', self.ValidWiring)
        self.assertIsNot(reflector, None)
        self.assertEqual(reflector.name, 'OK')
        self.assertEqual(reflector.wiring, self.ValidWiring)
        self.assertEqual(reflector.get_circuit(test_pin), expected_out_pin)


if __name__ == '__main__':
    unittest.main()
