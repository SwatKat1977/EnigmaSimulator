#  Copyright (C) 2015-2018 Electronic Engima Development Team
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  //////////////////////////////////////////////////////////////////////////
import unittest
from simulation.reflector_factory import ReflectorFactory


# ******************************
# Unit tests for the Rotor class
# ******************************
class UnitTest_ReflectorFactory(unittest.TestCase):

    def setUp(self):
        self._factory = ReflectorFactory()


    ## Test build_from_json : Rotor json file is missing or isn't readable.
    #  build_from_json should generate an 'Unable to open rotor file'  error
    #  message because the file is either missing or cannot be read.
    #  @param self The object pointer.
    def test_ReflectorFactory_build_from_json_Success(self):
        json_file = '../data/reflectors/Wide_B.json'

        reflector = self._factory.build_from_json(json_file)

        # Rotor should not be None
        self.assertIsNot(reflector, None)


    ##
    # Test CreateFromXML : Reflectors XML file is missing or isn't readable.
    # CreateFromXML should raise an IO error exception because the file is
    # either missing or cannot be read.
    # @param self The object pointer.
    def test_ReflectorFactory_build_from_json_FileNotFound(self):
        reflector = self._factory.build_from_json('FileNotFound')

        self.assertIs(reflector, None)

        expected = 'Unable to read file, reason: No such file or directory'
        if expected not in self._factory.last_error_message:
            self.fail("Did not detect 'Unable to read file'")


    ## Test build_from_json : Rotors json file doesn't is a valid json file.
    #  build_from_json should raise a 'json Failed to parse' because the file
    #  does contain a valid XML file.
    #  @param self The object pointer.
    def test_ReflectorFactory_build_from_json_UnableToParse(self):
        json_file = 'Core/unit_tests/test_data/Reflector_InvalidJson.json'

        reflector = self._factory.build_from_json(json_file)

        # Rotor should be None
        self.assertIs(reflector, None)

        expected_msg = "Unable to parse json, reason"
        if expected_msg not in self._factory.last_error_message:
            msg = f"Did not detect '{expected_msg}'"
            self.fail(msg)


    ## Test build_from_json : Rotors XML file is missing expected root tag.
    #  CreateFromXML should raise an error of 'missing root element' because
    #  the expected XML root cannot be found.
    #  @param self The object pointer.
    def test_ReflectorFactory_build_from_json_ValidationError(self):
        json_file = 'Core/unit_tests/test_data/Reflector_ValidationError.json'

        reflector = self._factory.build_from_json(json_file)

        # Rotors should be None
        self.assertIs(reflector, None)

        expected_msg = f"Failed to validate against schema,"
        if expected_msg not in self._factory.last_error_message:
            self.fail("Did not detect 'Failed to validate against'")


    ##
    # Test CreateFromXML : Return is status message.
    # CreateFromXML received error status back check.
    # @param self The object pointer.
    def test_ReflectorFactory_build_from_json_InputPinInUse(self):
        json_file = 'Core/unit_tests/test_data/Reflector_InPinInUse.json'

        reflector = self._factory.build_from_json(json_file)

        self.assertIs(reflector, None)

        expected = 'Circuit (24:1) input pin is already defined'
        if expected not in self._factory.last_error_message:
            err = f"Did not detect '{expected}'"
            self.fail(err)


    ##
    # Test CreateFromXML : Return is status message.
    # CreateFromXML received error status back check.
    # @param self The object pointer.
    def test_ReflectorFactory_build_from_json_OutputPinInUse(self):
        json_file = 'Core/unit_tests/test_data/Reflector_OutPinInUse.json'

        reflector = self._factory.build_from_json(json_file)

        # Rotors should be None
        self.assertIs(reflector, None)

        expected = 'Circuit (21:26) output pin is already defined'
        if expected not in self._factory.last_error_message:
            err = f"Did not detect '{expected}'"
            self.fail(err)










'''
    ##
    # Test CreateFromXML : Reflectors XML file doesn't is a valid XML file.
    # CreateFromXML should raise a 'XML Failed to parse' because the file does
    # contain a valid XML file.
    # @param self The object pointer.
    def test_CreateFromXML_InvalidXML(self):
        xmlFile = 'TestData/Reflectors_InvalidXML.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if 'XML Failed to parse ' not in status:
            self.fail("Did not detect 'XML Failed to parse'")


    ##
    # Test CreateFromXML : Reflectors XML file is missing expected root tag.
    # CreateFromXML should raise an error of 'missing root element' because the
    # expected XML root cannot be found.
    # @param self The object pointer.
    def test_CreateFromXML_InvalidRoot(self):
        xmlFile = 'TestData/Reflectors_InvalidRoot.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if 'missing root element' not in status:
            self.fail("Did not detect 'missing root element'")


    ##
    # Test CreateFromXML : Reflector is missing name attribute.
    # CreateFromXML should raise an error of 'Reflector doesn't have a name
    # attribute!' because a reflector is missing the name attribute.
    # @param self The object pointer.
    def test_CreateFromXML_NoReflectorName(self):
        xmlFile = 'TestData/Reflectors_NoReflectorName.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if "Reflector doesn't have a name attribute!" not in status:
            self.fail("Did not detect 'Reflector doesn't have a name attribute!'")


    ##
    # Test CreateFromXML : Invalid xml tag (not reflector) caught.
    # CreateFromXML Invalid XML tag caught in status.
    # @param self The object pointer.
    def test_CreateFromXML_InvalidXMLTag(self):
        xmlFile = 'TestData/Reflectors_InvalidReflector.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Rotors should be None
        self.assertIs(reflectors, None)

        if 'Invalid XML tag : deflector' not in status:
            self.fail("Did not detect 'Invalid XML tag : deflector'")

    ##
    # Test CreateFromXML : Reflector has invalid sub tag.
    # CreateFromXML should raise an error of 'Invalid xml tag '__CIRCUIT'
    # because a reflector has an invalid xml subtag (__circuit).
    # @param self The object pointer.
    def test_CreateFromXML_ReflectorSubTagInvalid(self):
        xmlFile = 'TestData/Reflectors_ReflectorSubTagInvalid.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if "Invalid xml tag '__CIRCUIT'" not in status:
            self.fail("Did not detect 'Invalid xml tag '__CIRCUIT''")


    ##
    # Test CreateFromXML : Reflector circuit validation failed.
    # CreateFromXML should raise an error of 'Circuit wiring in/out invalid!'
    # because one of the reflector circuits couldn't be validated, e.g. an
    # incorrect pin (numerical or outside range A-Z).
    # @param self The object pointer.
    def test_CreateFromXML_ReflectorCircuitInvalid(self):
        xmlFile = 'TestData/Reflectors_InvalidCircuit.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if "Circuit wiring in/out invalid!" not in status:
            self.fail("Did not detect 'Circuit wiring in/out invalid!'")


    ##
    # Test CreateFromXML : Reflector has duplicate circuit.
    # CreateFromXML should raise an error of 'One end of circuit (x:y) already
    # defined' because one of the reflector circuits already exists.
    # @param self The object pointer.
    def test_CreateFromXML_DuplicateCircuit(self):
        xmlFile = 'TestData/Reflectors_DuplicateCircuit.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if "One end of circuit (4:9) already defined" not in status:
            self.fail("Did not detect 'One end of circuit (4:9) already defined'")


    ##
    # Test CreateFromXML : Reflector has circuit with missing tag.
    # CreateFromXML should raise an error of 'Circuit wiring tag missing
    # attrib!' because one of the circuits is missing a mandatory tag.
    # @param self The object pointer.
    def test_CreateFromXML_CircuitWiringTagMissing(self):
        xmlFile = 'TestData/Reflectors_CircuitWiringTagMissing.xml'

        reflectors, status = self._factory.CreateFromXML(xmlFile)

        # Reflectors should be None
        self.assertIs(reflectors, None)

        if "Circuit wiring tag missing attrib!" not in status:
            self.fail("Did not detect 'Circuit wiring tag missing attrib!'")
'''

if __name__ == '__main__':
    unittest.main()
