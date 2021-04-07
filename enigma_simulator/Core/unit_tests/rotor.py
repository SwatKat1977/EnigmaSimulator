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
from Core.rotor_contact import RotorContact
from Core.rotor import Rotor


# ******************************
# Unit tests for the Rotor class
# ******************************
class UnitTest_Rotor(unittest.TestCase):

    # Rotors XML file
    VALID_ROTOR_FILENAME = '../Data/rotors/Enigma1_I.json'

    valid_rotor_wiring = {
        1: 5,
        2: 11,
        3: 13,
        4: 6,
        5: 12,
        6: 7,
        7: 4,
        8: 17,
        9: 22,
        10: 26,
        11: 14,
        12: 20,
        13: 15,
        14: 23,
        15: 25,
        16: 8,
        17: 24,
        18: 21,
        19: 19,
        20: 16,
        21: 1,
        22: 9,
        23: 2,
        24: 18,
        25: 3,
        26: 10}

    ##
    # Python unittest setup fixture.
    # Read test rotors so we have wiring and rotors for use in the tests.
    # @param self The object pointer.
    def setUp(self):
        self._valid_rotor = Rotor('Enigma 1 Rotor I', self.valid_rotor_wiring,
                                  ["Q"])


    ##
    # Python unittest tearDown fixture.
    # Teardown code will go here...
    # @param self The object pointer.
    def tearDown(self):
        pass


    ##
    # Test Constructor : Wiring matrix too small.
    # The constructor should raise the exception 'Incomplete wiring diagram'
    # when the wiring matrix is too small (not 26 contacts).
    # @param self The object pointer.
    def test_Constructor_WiringMatrixTooSmall(self):
        # Invalid wiring dictionary.
        invalidWiring =\
        {
            1 : 25,
            2 : 18,
            3 : 21,
            4 : 8
        }

        # Attempt to create a rotor, it should raise a ValueError exception.
        with self.assertRaises(ValueError) as context:
            rotor = Rotor('wiringMatrixTooSmall', invalidWiring,
                          [RotorContact.G])

        # Verify that the the exception was caught.
        if 'Incomplete wiring diagram' not in str(context.exception):
            self.fail("Did not detect 'Incomplete wiring diagram'")


    ##
    # Test Constructor : Wiring matrix not a dictionary.
    # The constructor should raise the exception 'Incompatible rotor wiring
    # diagram' when the wiring matrix isn't a dictionary.
    # @param self The object pointer.
    def test_Constructor_WiringMatrixInvalidType(self):

        # Attempt to create a rotor, it should raise a ValueError exception.
        with self.assertRaises(ValueError) as context:
            rotor = Rotor('WiringMatrixInvalidType', 'invalidWiring',
                          RotorContact.G)

        # Verify that the the exception was caught.
        if 'Incompatible rotor wiring diagram' not in str(context.exception):
            self.fail("Did not detect 'Incompatible rotor wiring diagram'")


    ##
    # Test Constructor : Valid parameters.
    # The constructor was successful.
    # @param self The object pointer.
    def test_Constructor_ValidParameters(self):

        # Attempt to create a rotor, it should not raise any exceptions.
        try:
            rotor = Rotor('ValidParameters', self._valid_rotor.wiring,
                          RotorContact.G)

        except Exception as ex:
            # Something has gone wrong as an exception was caught.
            self.fail('Unexpected exception was caught: {0}'.format(ex))


    def test_Step_Verify(self):
        # self._valid_rotor.

        # Verify just stepping one position.
        self.assertEqual(self._valid_rotor.position, 1)
        self._valid_rotor.step()
        self.assertEqual(self._valid_rotor.position, 2)

        # Verify stepping one position wrapping back to start.
        self._valid_rotor.position = 26
        self.assertEqual(self._valid_rotor.position, 26)
        self._valid_rotor.step()
        self.assertEqual(self._valid_rotor.position, 1)


    def test_WillStepNext_Verify(self):
        # Verify negative status (won't step).
        self.assertFalse(self._valid_rotor.will_step_next())

        # Verify positive status (will step).
        self._valid_rotor.position = RotorContact.Q.value
        self.assertTrue(self._valid_rotor.will_step_next())


    def WillStepNext(self):
        return self.__position in self.__notchLocations


    def test_VerifyGetters(self):
        # Verify Getter : Name
        self.assertEqual(self._valid_rotor.name, 'Enigma 1 Rotor I')

        # Verify Getter : NotchLocations
        self.assertEqual(self._valid_rotor.notches, [RotorContact.Q.name])

        # Verify Getter : Position
        self.assertEqual(self._valid_rotor.position, 1)

        # Verify Getter : RingSetting
        self.assertEqual(self._valid_rotor.ring_setting, 1)

 
    def test_Position_Setter(self):
        # Verify Setter : Position outside lower range.
        with self.assertRaises(ValueError) as context:
            self._valid_rotor.position = 0

        if 'Invalid rotor positions' not in str(context.exception):
            self.fail("Did not detect 'Invalid rotor positions'")

        # Verify Setter : Position outside upper range.
        with self.assertRaises(ValueError) as context:
            self._valid_rotor.position = 27

        if 'Invalid rotor positions' not in str(context.exception):
            self.fail("Did not detect 'Invalid rotor positions'")

        # Verify Setter : Position is valid and changed.
        self._valid_rotor.position = 12
        self.assertEqual(self._valid_rotor.position, 12)


    def test_RingSetting_Setter(self):
        # self._valid_rotor

        # Verify Setter : RingSetting outside lower range.
        with self.assertRaises(ValueError) as context:
            self._valid_rotor.ring_setting = 0

        if 'Invalid ring positions' not in str(context.exception):
            self.fail("Did not detect 'Invalid ring positions'")

        # Verify Setter : Position outside upper range.
        with self.assertRaises(ValueError) as context:
            self._valid_rotor.ring_setting = 27

        if 'Invalid ring positions' not in str(context.exception):
            self.fail("Did not detect 'Invalid ring positions'")

        # Verify Setter : Position is valid and changed.
        self._valid_rotor.ring_setting = 12
        self.assertEqual(self._valid_rotor.ring_setting, 12)


    def test_ForwardCircuit_NoOffsetNoRingSetting(self):
        # Default position is 1, but make 100% sure do it again!
        self._valid_rotor.position = 1

        # Verify a couple of different values: Contact 1 ('A')
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.A),
                         RotorContact(self._valid_rotor.wiring[RotorContact.A.value]))

        # Verify a couple of different values: Contact 13 ('M')
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.N),
                         RotorContact(self._valid_rotor.wiring[RotorContact.N.value]))

        # Verify a couple of different values: Contact 26 ('Z')
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.Z),
                         RotorContact(self._valid_rotor.wiring[RotorContact.Z.value]))


    ##
    # Test ForwardCircuit : Initial position not wrapping and no ring setting.
    # The rotor is in a position other than 1, but it's not enough for the
    # position to wrap to the beginning of the rotor.  For this test no ring
    # setting has been set.
    # @param self The object pointer.
    def test_ForwardCircuit_NoneStartWrappingOffsetNoRingSetting(self):

        # Default position is 1, but make 100% sure do it again!
        self._valid_rotor.position = 2

        # Verify a couple of different values: Contact 1 ('A')
        expected_contact = RotorContact(self._valid_rotor.wiring[1 + (self._valid_rotor.position -1)] -1)
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.A),
                         expected_contact)

        # Verify a couple of different values: Contact 13 ('M')
        expected_contact = RotorContact(self._valid_rotor.wiring[13 + (self._valid_rotor.position -1)] -1)
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.M),
                         expected_contact)


    ##
    # Test ForwardCircuit : Initial position not wrapping and no ring setting.
    # The rotor is in a position other than 1, but it's not enough for the
    # position to wrap to the beginning of the rotor.  For this test no ring
    # setting has been set.
    # @param self The object pointer.
    def test_ForwardCircuit_HasStartWrappingOffsetNoRingSetting(self):

        # Default position is 1, but make 100% sure do it again!
        # Set position to 20 'T'
        self._valid_rotor.position = 20

        # Verify that on pressing contact 9 'I' we get the encoded contact of
        # 19 'S' out taking into account the position of the rotor.  
        # Explanation:
        # Contact 9 pressed with position of 20 gives us 28 (-1 as 1 is 'none')
        # Since we can't have that position we wrap it around to 2 (28 - 26).
        # Contact 2 is wired to 11, but then reversing the position to get back
        # to the right contact gives you -8 (again -1 as 1 is 'no postion), 
        # which wraps to contact no. of 18.
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.I),
                        RotorContact.R)

        # Verify that on pressing contact 20 'T' we get the encoded contact of
        # 22 'V' out taking into account the position of the rotor.  
        # Explanation:
        # Contact 20 pressed with position of 20 gives us 39 (-1 as 1 is 'none')
        # Since we can't have that position we wrap it around to 13 (39 - 26).
        # Contact 13 is wired to 15, but then reversing the position to get back
        # to the right contact gives you -4 (again -1 as 1 is 'no postion),
        # which wraps to contact no. of 22.
        self.assertEqual(self._valid_rotor.get_forward_circuit(RotorContact.T),
                         RotorContact.V)


    def test_ReturnCircuit_NoOffsetNoRingSetting(self):
        # Default position is 1, but make 100% sure do it again!
        self._valid_rotor.position = 1

        # Verify a couple of different values: Contact 1 ('A')
        self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.A),
                         RotorContact.U)

        # Verify a couple of different values: Contact 13 ('M')
        self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.M),
                         RotorContact.C)

        # Verify a couple of different values: Contact 26 ('Z')
        self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.Z),
                         RotorContact.J)

    ##
    # Test ReturnCircuit : Initial position not wrapping and no ring setting.
    # The rotor is in a position other than 1, but it's not enough for the
    # position to wrap to the beginning of the rotor.  For this test no ring
    # setting has been set.
    # @param self The object pointer.
    def test_ReturnCircuit_NoneStartWrappingOffsetNoRingSetting(self):

        # Default position is 1, but make 100% sure do it again!
        self._valid_rotor.position = 1

        # Verify a couple of different values: Contact 1 ('A')
        pressed_key = RotorContact.A
        contact = pressed_key.value + (self._valid_rotor.position -1)
        out_contact = self._valid_rotor.reverse_wiring[contact]
        self.assertEqual(self._valid_rotor.get_return_circuit(pressed_key),
                         RotorContact(out_contact))

        # Verify a couple of different values: Contact 13 ('M')
        pressed_key = RotorContact.M
        contact = pressed_key.value + (self._valid_rotor.position -1)
        out_contact = self._valid_rotor.reverse_wiring[contact]
        # (wiring.keys()[wiring.values().index(contact)]
        #             - (self._valid_rotor.position -1))
        self.assertEqual(self._valid_rotor.get_return_circuit(pressed_key),
                         RotorContact(out_contact))


    ##
    # Test ReturnCircuit : Initial position not wrapping and no ring setting.
    # The rotor is in a position other than 1, but it's not enough for the
    # position to wrap to the beginning of the rotor.  For this test no ring
    # setting has been set.
    # @param self The object pointer.
    def test_ReturnCircuit_HasStartWrappingOffsetNoRingSetting(self):

        # Default position is 1, but make 100% sure do it again!
        # Set position to 20 'T'
        self._valid_rotor.position = RotorContact.T.value

        # Verify that on pressing contact 9 'I' we get the encoded contact of
        # 4 'D' out taking into account the position of the rotor.
        # Explanation:
        # Contact 9 pressed with position of 20 gives us 28 (-1 as 1 is 'none')
        # Since we can't have that position we wrap it around to 2 (28 - 26).
        # Contact 2 is wired to 23, but then reversing the position to get back
        # to the right contact gives you -4 (again -1 as 1 is 'no postion).
        self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.I), 
                         RotorContact.D)

        # Verify that on pressing contact 20 'T' we get the encoded contact of
        # 10 'J' out taking into account the position of the rotor.
        # Explanation:
        # Contact 20 pressed with position of 20 gives us 39 (-1 as 1 is 'none')
        # Since we can't have that position we wrap it around to 13 (39 - 26).
        # Contact 13 is wired to 3, but then reversing the position to get back
        # to the right contact gives you -16  (again -1 as 1 is 'no postion),
        # which wraps to contact no. of 10.
        self.assertEqual(self._valid_rotor.get_return_circuit(RotorContact.T),
                         RotorContact.J)


if __name__ == '__main__':
    unittest.main()
