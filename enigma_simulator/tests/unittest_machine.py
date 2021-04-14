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
from simulation.enigma_machine import EnigmaMachine
from simulation.rotor_contact import RotorContact
#from Core.MachineSetup import *
from simulation.reflector_factory import ReflectorFactory
from simulation.plugboard import Plugboard

class UnitTest_EnigmaMachine(unittest.TestCase):
    ''' Unit tests for the Enigma Machine class. '''

    # Rotors XML file
    Rotor_enigma1_I_file = '../data/rotors/Enigma1_I.json'
    Rotor_enigma1_II_file = '../data/rotors/Enigma1_II.json'
    Rotor_enigma1_III_file = '../data/rotors/Enigma1_III.json'
    REFLECTORS_FILE = '../../Data/reflectors.xml'

    '''
    ##
    # Python unittest setup fixture.
    # Read test rotors so we have wiring and rotors for use in the tests.
    # @param self The object pointer.
    def setUp(self):
        self._rotor_factory = RotorFactory()
        self._reflector_factory = ReflectorFactory()

        self._rotor_enigma1_i = self._rotor_factory.build_from_json(self.Rotor_enigma1_I_file)
        if not self._rotor_enigma1_i:
            err = f'Unable to create rotors from XML: {self._rotor_factory.last_error_message}'
            raise RuntimeError(err)

        self._rotor_enigma1_ii = self._rotor_factory.build_from_json(self.Rotor_enigma1_II_file)
        if not self._rotor_enigma1_ii:
            err = f'Unable to create rotors from XML: {self._rotor_factory.last_error_message}'
            raise RuntimeError(err)

        self._rotor_enigma1_iii = self._rotor_factory.build_from_json(self.Rotor_enigma1_III_file)
        if not self._rotor_enigma1_iii:
            err = f'Unable to create rotors from XML: {self._rotor_factory.last_error_message}'
            raise RuntimeError(err)

        self.__plugboard = Plugboard()


        # Create machine setup.
        self.__setup = MachineSetup(EnigmaModel.Enigma1, 
                                    ["Rotor I", "Rotor II","Rotor III"],
                                    self.__plugboard)
        
        # Read reflectors XML file.
        reflectors, status = self._reflector_factory.CreateFromXML(
            self.REFLECTORS_FILE)
        if reflectors == None:
            errStatus = "Unable to read reflectors XML file: {0}".format(status)
            raise RuntimeError(errStatus)
        
        self.__reflector = reflectors['Wide Reflector B']
    '''

    def test_EnigmaMachine_configure_machine_OK(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)
 
        config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

        if not config_return:
            self.fail(enigma_machine.last_error)

        self.assertIsNot(enigma_machine.plugboard, None)
        self.assertIsNot(enigma_machine.reflector, None)
        self.assertIs(enigma_machine.debug_messages, False)

        enigma_machine.debug_messages = True
        self.assertIs(enigma_machine.debug_messages, True)
        enigma_machine.debug_messages = False

        self.assertIs(enigma_machine.configured, True)


    def test_EnigmaMachine_configure_machine_InvalidMachineType(self):
        try:
            enigma_machine = EnigmaMachine('Invalid macgine')
            self.fail('Incorrectly constructed Enigma machine')

        except ValueError as err:
            expected = 'Enigma model is not valid'

            if expected not in str(err):
                err_msg = f"Did not detect '{expected}'"
                self.fail(err_msg)


    def test_EnigmaMachine_configure_machine_InvalidRotor(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['Ia', 'II', 'III'], 'Wide_B')
        self.assertIs(config_return, False)
        self.assertIs(enigma_machine.configured, False)

        expected = 'Rotor read failure | Unable to open rotor file'
        if expected not in enigma_machine.last_error:
            err = f"Did not detect '{expected}'"
            self.fail(err)


    def test_EnigmaMachine_configure_machine_InvalidNoOfRotors(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['I', 'II'], 'Wide_B')
        self.assertIs(config_return, False)
        self.assertIs(enigma_machine.configured, False)

        expected = 'Invalid number of rotors specified, requires 3 rotors'
        if expected not in enigma_machine.last_error:
            err = f"Did not detect '{expected}'"
            self.fail(err)


    def test_EnigmaMachine_configure_machine_InvalidReflector(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_Ba')
        self.assertIs(config_return, False)
        self.assertIs(enigma_machine.configured, False)

        expected = 'Reflector read failure | Unable to read file, reason:'
        if expected not in enigma_machine.last_error:
            err = f"Did not detect '{expected}'"
            self.fail(err)


    def test_EnigmaMachine_3_Rotor_Encoding_No_Turnover(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

        if not config_return:
            self.fail(enigma_machine.last_error)

        self.assertIs(enigma_machine.configured, True)

        string_to_encode = 'AAAAA'
        expected_encoded_string = 'BDZGO'

        encoded = ''
        for char in string_to_encode.upper():
            encoded += enigma_machine.press_key(RotorContact[char]).name

        self.assertEqual(encoded, expected_encoded_string)


    def test_EnigmaMachine_3_Rotor_Encoding_Right_Rotor_Turnover(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

        if not config_return:
            self.fail(enigma_machine.last_error)

        self.assertIs(enigma_machine.configured, True)

        enigma_machine.set_rotor_position(0, 1)
        enigma_machine.set_rotor_position(1, 1)
        enigma_machine.set_rotor_position(2, RotorContact.T.value)

        string_to_encode = 'AAAAA'
        expected_encoded_string = 'BMUQO'

        encoded = ""
        for char in string_to_encode.upper():
            encoded += enigma_machine.press_key(RotorContact[char]).name

        # AAAAA should be encrypted into BMUQO.
        self.assertEqual(encoded, expected_encoded_string)

        # Initially the rotors A | A | A.  On the third letter there is a
        # turnover of middle so should end A | B | Y.
        self.assertEqual(enigma_machine.get_rotor_position(0), RotorContact.A.value)
        self.assertEqual(enigma_machine.get_rotor_position(1), RotorContact.B.value)
        self.assertEqual(enigma_machine.get_rotor_position(2), RotorContact.Y.value)


    def test_EnigmaMachine_set_rotor_position_ErrorChecking(self):
        try:
            enigma_machine = EnigmaMachine('Enigma1')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        self.assertIsNot(enigma_machine, None)

        config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

        if not config_return:
            self.fail(enigma_machine.last_error)
            return

        test_passed = False
        err_msg = 'set_rotor_position() rotor position was unexpectedly set'

        try:
            enigma_machine.set_rotor_position(1, 0)

        except ValueError as excpt:
            expected = 'Invalid rotor positions'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
            else:
                test_passed = True

        if not test_passed:
            self.fail(err_msg)

        test_passed = False
        err_msg = 'set_rotor_position() rotor position was unexpectedly set'

        try:
            enigma_machine.set_rotor_position(1, 27)

        except ValueError as excpt:
            expected = 'Invalid rotor positions'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
            else:
                test_passed = True

        if not test_passed:
            self.fail(err_msg)

        test_passed = False
        err_msg = 'set_rotor_position() Invalid rotor was unexpectedly used'

        try:
            enigma_machine.set_rotor_position(-1, 10)

        except ValueError as excpt:
            expected = 'Invalid rotor'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
            else:
                test_passed = True

        if not test_passed:
            self.fail(err_msg)

        test_passed = False
        err_msg = 'set_rotor_position() Invalid rotor was unexpectedly used'

        try:
            enigma_machine.set_rotor_position(3, 10)

        except ValueError as excpt:
            expected = 'Invalid rotor'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
            else:
                test_passed = True

        if not test_passed:
            self.fail(err_msg)



        '''
    def set_rotor_position(self, rotor_no, position):
        # Validate rotor positions.
        if position < 1 or position > NO_OF_ROTOR_CONTACTS:
            raise ValueError("Invalid rotor positions")

        if rotor_no < 0 or rotor_no > (len(self._rotors) - 1):
            raise ValueError("Invalid rotor")
        '''

    '''
    def test_3RotorEncryptString_DoubleStep(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Initially the rotors A | D | T.
        machine.SetRotorPosition(RotorPosition.One, 1)
        machine.SetRotorPosition(RotorPosition.Two, 4)
        machine.SetRotorPosition(RotorPosition.Three, 20)

        ContactToCharacter = RotorContact.Instance().ContactToCharacter

        stringToEncode = 'AAAAA'
        expectedEncodedString = 'EEQIB'

        encrypted = ""
        for char in stringToEncode.upper():
            if char >= 'A' and char <= 'Z':
                char = RotorContact.Instance().CharacterToContact(char)
                encrypted += ContactToCharacter(machine.PressKey(char))

        # Initially the rotors A | D | T.  On the fourth letter there is a
        # double step so should end B | F | Y.
        self.assertEqual(ContactToCharacter(machine.GetRotor(0).Position), 'B')
        self.assertEqual(ContactToCharacter(machine.GetRotor(1).Position), 'F')
        self.assertEqual(ContactToCharacter(machine.GetRotor(2).Position), 'Y')

        # AAAAA should be encrypted into BMUQO.
        self.assertEqual(encrypted, expectedEncodedString)


    def test_SetRotorPosition_InvalidPosition(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Attempt to set an invalid rotor position, it should raise a
        # ValueError.
        with self.assertRaises(ValueError) as context:
            machine.SetRotorPosition(0, 0)

        # Verify that the the exception was caught.
        if "Invalid rotor positions" not in context.exception:
            self.fail("Did not detect 'Invalid rotor positions'")


    def test_SetRotorPosition_InvalidRotor(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Attempt to set an invalid rotor position, it should raise a
        # ValueError.
        with self.assertRaises(ValueError) as context:
            machine.SetRotorPosition(4, 10)

        # Verify that the the exception was caught.
        if "Invalid rotor" not in context.exception:
            self.fail("Did not detect 'Invalid rotor'")


    def test_SetRotorPosition_Valid(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Attempt to set an valid rotor position.
        machine.SetRotorPosition(2, 10)


    def test_GetRotor_InvalidRotor(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Attempt to set an invalid rotor position, it should raise a
        # ValueError.
        with self.assertRaises(ValueError) as context:
            machine.GetRotor(4)

        # Verify that the the exception was caught.
        if "Incorrect rotor number." not in context.exception:
            self.fail("Did not detect 'Incorrect rotor number.'")


    def test_Verify_GettersSetters(self):
        # Create (valid) Enigma machine.
        machine = EnigmaMachine(self.__setup, self.__rotors, self.__reflector,
            True)
        self.assertIsNot(machine, None)

        # Plugboard - check is set.
        self.assertEqual(machine.Plugboard, self.__plugboard)

        # Reflector - check name is 'test'.
        self.assertEqual(machine.Reflector.Name, 'Wide Reflector B')

        # Reflector - check it is 'True', then set to 'False' and recheck.
        self.assertEqual(machine.Trace, True)
        machine.Trace = False
        self.assertEqual(machine.Trace, False)
    '''

if __name__ == '__main__':
    unittest.main()

# 435 lines