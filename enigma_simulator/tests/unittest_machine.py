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

    def test_machine_3_rotor_encrypt_right_rotor_turnover(self):
        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        config_return = machine.configure('Enigma1', ['I', 'II', 'III'], 'UKW-B')

        if not config_return:
            self.fail(machine.last_error)

        self.assertIs(machine.configured, True)

        machine.set_rotor_position(0, 0)
        machine.set_rotor_position(1, 0)
        machine.set_rotor_position(2, RotorContact.T.value)

        string_to_encode = 'AAAAA'
        expected_encoded_string = 'BMUQO'

        encoded = ""
        for char in string_to_encode.upper():
            encoded += machine.press_key(RotorContact[char]).name

        # AAAAA should be encrypted into BMUQO.
        self.assertEqual(encoded, expected_encoded_string)

        # Initially the rotors A | A | A.  On the third letter there is a
        # turnover of middle so should end A | B | Y.
        self.assertEqual(machine.get_rotor_position(0), RotorContact.A.value)
        self.assertEqual(machine.get_rotor_position(1), RotorContact.B.value)
        self.assertEqual(machine.get_rotor_position(2), RotorContact.Y.value)

    def test_machine_set_rotor_position_invalid_rotor_position(self):
        ''' Machine::set_rotor_position() | Invalid rotor position '''

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II', 'III'], 'UKW-B')
        if not status:
            self.fail(machine.last_error)

        try:
            machine.set_rotor_position(1, -1)
            self.fail("ValueError exception Invalid rotor positions not raised")

        except ValueError as excpt:
            expected = 'Invalid rotor positions'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
                self.fail(err_msg)

        try:
            machine.set_rotor_position(1, 26)
            self.fail("ValueError exception Invalid rotor positions not raised")

        except ValueError as excpt:
            expected = 'Invalid rotor positions'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
                self.fail(err_msg)

    def test_machine_set_rotor_position_invalid_rotor_number(self):
        ''' Machine::set_rotor_position() | Invalid rotor number '''

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II', 'III'], 'UKW-B')
        if not status:
            self.fail(machine.last_error)

        try:
            machine.set_rotor_position(-1, 10)
            self.fail("ValueError exception Invalid rotor positions not raised")

        except ValueError as excpt:
            expected = 'Invalid rotor'
            if expected not in str(excpt):
                err_msg = f"Did not detect '{expected}, got: {excpt}'"
                self.fail(err_msg)



    def test_machine_3_rotor_encrypt_double_step(self):

        machine = Machine()
        self.assertIsNot(machine, None)
        machine._logger._write_to_console = False

        status = machine.configure('Enigma1', ['I', 'II', 'III'], 'UKW-B')
        if not status:
            self.fail(machine.last_error)

        # Set the rotors A | D | U.
        machine.set_rotor_position(0, RotorContact.A.value)
        machine.set_rotor_position(1, RotorContact.D.value)
        machine.set_rotor_position(2, RotorContact.U.value)

        string_to_encrypt = 'AAAA'
        expected_encrypted_string = 'EQIB'

        encrypted = ""
        for char in string_to_encrypt.upper():
            char = RotorContact[char]
            encrypted += machine.press_key(char).name

        # The rotors start at A | D | U.  On the fourth letter there is a
        # double step so should end B | F | Y.
        self.assertEqual(machine.get_rotor_position(0), RotorContact.B.value)
        self.assertEqual(machine.get_rotor_position(1), RotorContact.F.value)
        self.assertEqual(machine.get_rotor_position(2), RotorContact.Y.value)

        # AAAAA should be encrypted into BMUQO.
        self.assertEqual(encrypted, expected_encrypted_string)


if __name__ == '__main__':
    unittest.main()

# 435 lines