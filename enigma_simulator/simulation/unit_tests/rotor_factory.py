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
from Core.rotor_factory import RotorFactory


# ******************************
# Unit tests for the Rotor class
# ******************************
class UnitTest_RotorFactory(unittest.TestCase):

    def setUp(self):
        self._factory = RotorFactory()


    ## Test build_from_json : Rotor json file is missing or isn't readable.
    #  build_from_json should generate an 'Unable to open rotor file'  error
    #  message because the file is either missing or cannot be read.
    #  @param self The object pointer.
    def test_RotorFactory_build_from_json_Success(self):
        json_file = '../data/rotors/Enigma1_I.json'

        rotor = self._factory.build_from_json(json_file)

        # Rotor should not be None
        self.assertIsNot(rotor, None)


    ## Test build_from_json : Rotor json file is missing or isn't readable.
    #  build_from_json should generate an 'Unable to open rotor file'  error
    #  message because the file is either missing or cannot be read.
    #  @param self The object pointer.
    def test_RotorFactory_build_from_json_FileNotFound(self):
        rotor = self._factory.build_from_json('FileNotFound')

        # Rotor should be None
        self.assertIs(rotor, None)

        expected_msg = "Unable to open rotor file 'FileNotFound', reason: " + \
                       "No such file or directory"
        if expected_msg not in self._factory.last_error_message:
            self.fail("Did not detect 'IO error, reason :'")


    ## Test build_from_json : Rotors json file doesn't is a valid json file.
    #  build_from_json should raise a 'json Failed to parse' because the file
    #  does contain a valid XML file.
    #  @param self The object pointer.
    def test_RotorFactory_build_from_json_UnableToParse(self):
        json_file = 'Core/unit_tests/test_data/Rotors_InvalidJson.json'

        rotor = self._factory.build_from_json(json_file)

        # Rotor should be None
        self.assertIs(rotor, None)

        expected_msg = f"Unable to parse rotor file {json_file}"
        if expected_msg not in self._factory.last_error_message:
            msg = f"Did not detect '{expected_msg}'"
            self.fail(msg)


    ## Test build_from_json : Rotors XML file is missing expected root tag.
    #  CreateFromXML should raise an error of 'missing root element' because
    #  the expected XML root cannot be found.
    #  @param self The object pointer.
    def test_RotorFactory_build_from_json_ValidationError(self):
        json_file = 'Core/unit_tests/test_data/Rotor_ValidationError.json'

        rotor = self._factory.build_from_json(json_file)

        # Rotors should be None
        self.assertIs(rotor, None)

        expected_msg = f"Rotor file {json_file} failed to validate against" + \
                        " expected schema."
        if expected_msg not in self._factory.last_error_message:
            self.fail("Did not detect 'Failed to validate against'")


    ##
    # Test CreateFromXML : Return is status message.
    # CreateFromXML received error status back check.
    # @param self The object pointer.
    def test_RotorFactory_build_from_json_InputPinInUse(self):
        json_file = 'Core/unit_tests/test_data/Rotor_InPinInUse.json'

        rotor = self._factory.build_from_json(json_file)

        # Rotors should be None
        self.assertIs(rotor, None)

        expected = 'Circuit (3:6) input pin is already defined'
        if expected not in self._factory.last_error_message:
            err = f"Did not detect '{expected}'"
            self.fail(err)


    ##
    # Test CreateFromXML : Return is status message.
    # CreateFromXML received error status back check.
    # @param self The object pointer.
    def test_RotorFactory_build_from_json_OutputPinInUse(self):
        json_file = 'Core/unit_tests/test_data/Rotor_OutPinInUse.json'

        rotor = self._factory.build_from_json(json_file)

        # Rotors should be None
        self.assertIs(rotor, None)

        expected = 'Circuit (19:23) output pin is already defined'
        if expected not in self._factory.last_error_message:
            err = f"Did not detect '{expected}'"
            self.fail(err)


if __name__ == '__main__':
    unittest.main()
