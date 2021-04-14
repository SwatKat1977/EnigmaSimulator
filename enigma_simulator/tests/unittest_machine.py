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
from simulation.enigma_machine import Machine
from simulation.rotor_contact import RotorContact
from simulation.plugboard import Plugboard

class UnitTestMachine(unittest.TestCase):
    ''' Unit tests for the Enigma Machine class. '''

    def setUp(self):
        self._plugboard = Plugboard()

    def test_configure_OK(self):
        ''' Machine::configure() | Happy path '''

        machine = Machine()
        machine._logger._write_to_console = False
        self.assertIsNot(machine, None)
 
        try:
            status = machine.configure('Enigma1',  ['I', 'II', 'III'], 'UKW-B')

        except ValueError as err:
            err = f'ValueError exception unexpectedly raised: {err}'
            self.fail(err)

        if not status:
            self.fail(machine.last_error)

        self.assertIsNot(machine.plugboard, None)
        self.assertIsNot(machine.reflector, None)
        self.assertIs(machine.configured, True)

    def test_configure_invalid_machine_type(self):
        ''' Machine::configure() | Invalid machine type. '''

        try:
            machine = Machine()
            machine._logger._write_to_console = False
            machine.configure('Unknown',  ['I', 'II', 'III'], 'UKW-B')
            self.fail('Incorrectly constructed Enigma machine')

        except ValueError as err:
            expected = 'Enigma model is not valid'

            if expected not in str(err):
                err_msg = f"Did not detect '{expected}'"
                self.fail(err_msg)

    def test_configure_invalid_rotor(self):
        ''' Machine::configure() | Invalid rotor specified '''

        machine = Machine()
        machine._logger._write_to_console = False
        status = machine.configure('Enigma1',  ['Ix', 'II', 'III'], 'UKW-B')
        self.assertIs(status, False)
        self.assertIs(machine.configured, False)

        expected = "Rotor 'Ix' is invalid, aborting!"
        if expected not in machine.last_error:
            err = f"Did not detect '{expected}'"
            self.fail(err)

    def test_configure_invalid_no_of_rotors(self):
        ''' Machine::configure() | Invalid no of rotors '''

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II'], 'Wide_B')
        self.assertIs(status, False)
        self.assertIs(machine.configured, False)

        expected = 'Invalid number of rotors specified, requires 3 rotors'
        if expected not in machine.last_error:
            err = f"Did not detect '{expected}'"
            self.fail(err)

    def test_configure_machine_invalid_reflector(self):
        ''' Machine::configure() | Invalid reflector '''

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II', 'III'], 'Wide_Ba')
        self.assertIs(status, False)
        self.assertIs(machine.configured, False)

        expected = "Reflector 'Wide_Ba' is invalid, aborting!"
        if expected not in machine.last_error:
            err = f"Did not detect '{expected}' | Last error : '{machine.last_error}'"
            self.fail(err)

    def test_3_rotor_encrypt_no_turnover(self):
        ''' Test 3 rotor Enigma 1 encrypt with no turnover '''

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II', 'III'], 'UKW-B')
        self.assertIs(status, True)
        self.assertIs(machine.configured, True)

        if not status:
            self.fail(machine.last_error)

        self.assertIs(machine.configured, True)

        string_to_encode = 'AAAAA'
        expected_encoded_string = 'BDZGO'

        encoded = ''
        for char in string_to_encode.upper():
            encoded += machine.press_key(RotorContact[char]).name

        self.assertEqual(encoded, expected_encoded_string)

    def test_machine_3_Rotor_Encoding_Right_Rotor_Turnover(self):
        try:
            enigma_machine = Machine('Enigma1')

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

    # def test_EnigmaMachine_set_rotor_position_ErrorChecking(self):
    #     try:
    #         enigma_machine = Machine('Enigma1')

    #     except ValueError as err:
    #         err = f'ValueError exception unexpectedly raised: {err}'
    #         self.fail(err)

    #     self.assertIsNot(enigma_machine, None)

    #     config_return = enigma_machine.configure_machine(['I', 'II', 'III'], 'Wide_B')

    #     if not config_return:
    #         self.fail(enigma_machine.last_error)
    #         return

    #     test_passed = False
    #     err_msg = 'set_rotor_position() rotor position was unexpectedly set'

    #     try:
    #         enigma_machine.set_rotor_position(1, 0)

    #     except ValueError as excpt:
    #         expected = 'Invalid rotor positions'
    #         if expected not in str(excpt):
    #             err_msg = f"Did not detect '{expected}, got: {excpt}'"
    #         else:
    #             test_passed = True

    #     if not test_passed:
    #         self.fail(err_msg)

    #     test_passed = False
    #     err_msg = 'set_rotor_position() rotor position was unexpectedly set'

    #     try:
    #         enigma_machine.set_rotor_position(1, 27)

    #     except ValueError as excpt:
    #         expected = 'Invalid rotor positions'
    #         if expected not in str(excpt):
    #             err_msg = f"Did not detect '{expected}, got: {excpt}'"
    #         else:
    #             test_passed = True

    #     if not test_passed:
    #         self.fail(err_msg)

    #     test_passed = False
    #     err_msg = 'set_rotor_position() Invalid rotor was unexpectedly used'

    #     try:
    #         enigma_machine.set_rotor_position(-1, 10)

    #     except ValueError as excpt:
    #         expected = 'Invalid rotor'
    #         if expected not in str(excpt):
    #             err_msg = f"Did not detect '{expected}, got: {excpt}'"
    #         else:
    #             test_passed = True

    #     if not test_passed:
    #         self.fail(err_msg)

    #     test_passed = False
    #     err_msg = 'set_rotor_position() Invalid rotor was unexpectedly used'

    #     try:
    #         enigma_machine.set_rotor_position(3, 10)

    #     except ValueError as excpt:
    #         expected = 'Invalid rotor'
    #         if expected not in str(excpt):
    #             err_msg = f"Did not detect '{expected}, got: {excpt}'"
    #         else:
    #             test_passed = True

    #     if not test_passed:
    #         self.fail(err_msg)



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