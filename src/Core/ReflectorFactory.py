'''
    <one line to give the program's name and a brief idea of what it does.>
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
import xml.etree.ElementTree as ElementTree
from Singleton import Singleton
from Reflector import Reflector
from RotorContact import RotorContact


# ***********************************************************************
# Singleton class for a factor to create reflectors.
# ***********************************************************************
@Singleton
class ReflectorFactory(object):

    # XML Element : Reflectors (root object)
    XML_ELEMENT_ROOT = 'REFLECTORS'

    # XML Element (and attribute): Reflector
    XML_ELEMENT_REFLECTOR = 'REFLECTOR'
    XML_ELEMENT_ATTRIB_REFLECTOR_NAME = 'NAME'

    # XML Element (and attributes): Circuit
    XML_ELEMENT_REFLECTOR_CIRCUIT = 'CIRCUIT'
    XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_IN = 'IN'
    XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_OUT = 'OUT'


    ##
    # Read a reflector XML file.  If the XML file is incorrectly formatted or
    # if there is a validity issue (duplicate wiring) then error is returned.
    # @param self The object pointer.
    # @param xmlFile XML filename string
    # @return Tuple of (rotorsList, statusString).  On success rotorsList will
    # be populated and status empty on failure rotorsList is none and a status.
    def CreateFromXML(self, xmlFile):
        reflectors = {}

        # Attempt to parse the XML file
        try:
            tree = ElementTree.parse(xmlFile)

        # Catch exception if file doesn't exist or can't be read.
        except IOError as ioException:
            errStr = 'IO error, reason : {0}'.format(ioException.strerror)            
            return (None, errStr)

        # Catch exception if file isn't correctly formed.
        except ElementTree.ParseError as parseException:
            errStr = 'XML Failed to parse \'{0}\', reason : {1}'.format(
                xmlFile, parseException.message)    
            return (None, errStr)

        # Get the root object
        root = tree.getroot()

        # Expecting correct root (reflectors), verify it!
        if root.tag.upper() != self.XML_ELEMENT_ROOT:
            return (None, 'missing root element ({0})'.format(
                self.XML_ELEMENT_ROOT))

        # Iterate through elements, one at a time.
        for element in root:

            # If element is 'REFLECTOR'.
            if element.tag.upper() == self.XML_ELEMENT_REFLECTOR:
                reflector = self.__ParseReflectorElement(element)

                # If reflector is not an instance of the Reflector class - e.g.
                # a string then it's a failure.
                if type(reflector) == str:
                    return (None, reflector)

                # It was OK, add to temporary list, which only gets added if
                # all entries are OK.
                reflectors[reflector.Name] = reflector 

            # Invalid tag - expecting 'reflector'.
            else:
                return (None, 'Invalid XML tag : {0}'.format(element.tag))

        # Everything went through successfully, return list of rotors.
        return (reflectors, '')


    ##
    # Parse a reflector element from the XML file, if it fails validation
    # checking then a string with the error message, otherwise a Reflector
    # class instance is created.
    # @param self The object pointer.
    # @param element Element to parse.
    # @return Success = Rotor instance, failure = string containing error.
    def __ParseReflectorElement(self, element):
        reflectorName = None
        circuits = {}

        # Convert the elements attribute keys to upper-case.
        elementAttribs = dict((key.upper(), value)
         for key, value in element.attrib.iteritems())

        # Check if reflector has a name, if it does then set it, or abort.
        if self.XML_ELEMENT_ATTRIB_REFLECTOR_NAME in elementAttribs:
            reflectorName = elementAttribs[self.XML_ELEMENT_ATTRIB_REFLECTOR_NAME]

        # No reflector name specified - invalid XMl.
        else:
            return "Reflector doesn't have a name attribute!"

        # Iterate through sub-elements, checking them.
        for subelement in element:

            subelementName = subelement.tag.upper()

            # Wiring circuit
            if subelementName == self.XML_ELEMENT_REFLECTOR_CIRCUIT:
                attribs = dict((key.upper(), value)
                 for key, value in subelement.attrib.iteritems())

                # Check that the circuit tag have the in and out attributes.
                if self.XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_IN not in attribs or \
                   self.XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_OUT not in attribs:
                    return "Circuit wiring tag missing attrib!"

                circuitIn = attribs[self.XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_IN]
                circuitOut = attribs[self.XML_ELEMENT_ATTRIB_REFLECTOR_CIRCUIT_OUT]

                # Convert the circuit letters to pins, if either fails then an
                # exception is generated.
                try:
                    circuitIn = RotorContact.Instance().CharacterToContact(
                        circuitIn)
                    circuitOut = RotorContact.Instance().CharacterToContact(
                        circuitOut)

                except ValueError:
                    return "Circuit wiring in/out invalid!"

                # Check that neither end of the circuit is already in use.
                if circuitIn in circuits or circuitOut in circuits.values():
                    return "One end of circuit ({0}:{1}) already defined".format(
                    circuitIn, circuitOut)

                circuits[circuitIn] = circuitOut

            # Invalid element.
            else:
                return "Invalid xml tag '{0}'".format(subelementName)

        return Reflector(reflectorName, circuits)


reflectorFactory = ReflectorFactory.Instance()
