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
from Rotor import *
from Singleton import Singleton
from RotorContact import RotorContact


@Singleton
class RotorFactory(object):

    # XML Element : Rotors (root object)
    XML_ELEMENT_ROOT = 'ROTORS'

    # XML Element (and attribute): Rotor
    XML_ELEMENT_ROTOR = 'ROTOR'
    XML_ELEMENT_ATTRIB_ROTOR_NAME = 'NAME'

    # XML Element: Rotor notch
    XML_ELEMENT_ROTOR_NOTCH = 'NOTCH'

    # XML Element (and attributes): Circuit
    XML_ELEMENT_ROTOR_CIRCUIT = 'CIRCUIT'
    XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_IN = 'IN'
    XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_OUT = 'OUT'


    ##
    # Read a rotors XML file.  If the XML file is incorrectly formatted or if
    # there is a validity issue (duplicate wiring) then False is returned.
    # @param xmlFile XML filename string
    # @return Success = True, failure = False
    def CreateFromXML(self, xmlFile):
        rotors = {}

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

        # Expecting correct root (rotors), verify it!
        if root.tag.upper() != self.XML_ELEMENT_ROOT:
            return (None, 'missing root element ({0})'.format(
                self.XML_ELEMENT_ROOT))

        # Iterate through elements, one at a time.
        for element in root:

            # If element is 'ROTOR'.
            if element.tag.upper() == self.XML_ELEMENT_ROTOR:
                rotor = self.__ParseRotorElement(element)

                # If rot an instance of rotor - e.g. a string then failure.
                if type(rotor) == str:
                    return (None, rotor)

                # It was OK, add to temporary list, which only gets added if
                # all entries are OK.
                rotors[rotor.Name] = rotor 

            # Invalid tag - expecting 'rotor'...
            else:
                return (None, 'Invalid XML tag : {0}'.format(element.tag))

        # Everything went through successfully, return list of rotors.
        return (rotors, '')


    ##
    # Parse a rotor element from the XML file, if it fails validation checking
    # then a string with the error message, otherwise a rotor class instance is
    # created.
    # @param element Element to parse.
    # @return Success = Rotor instance, failure = string containing error.
    def __ParseRotorElement(self, element):
        rotorName = None
        notches = []
        circuits = {}

        # Convert the elements attribute keys to upper-case.
        elementAttribs = dict((key.upper(), value)
         for key, value in element.attrib.iteritems())

        # Check if rotor has a name, if it does then set it, or abort.
        if self.XML_ELEMENT_ATTRIB_ROTOR_NAME in elementAttribs:
            rotorName = elementAttribs[self.XML_ELEMENT_ATTRIB_ROTOR_NAME]

        # No rotor name specified - invalid XMl.
        else:
            return "Rotor doesn't have name attribute!"

        # Iterate through sub-elements, checking them.
        for subelement in element:

            subelementName = subelement.tag.upper()

            # Wiring circuit
            if subelementName == self.XML_ELEMENT_ROTOR_CIRCUIT:
                attribs = dict((key.upper(), value)
                 for key, value in subelement.attrib.iteritems())

                # Check that the circuit tag have the in and out attributes.
                if self.XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_IN not in attribs or \
                   self.XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_OUT not in attribs:
                    return "Circuit wiring tag missing attrib!"

                circuitIn = attribs[self.XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_IN]
                circuitOut = attribs[self.XML_ELEMENT_ATTRIB_ROTOR_CIRCUIT_OUT]

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

            # Notch 
            elif subelementName == self.XML_ELEMENT_ROTOR_NOTCH:
                # Convert a character (should be a-zA-Z) to a pin number, if
                # if there is an issue or invalid then exception of ValueError
                # is raised.
                try:
                    notches.append(RotorContact.Instance().CharacterToContact(
                        subelement.text))

                except ValueError:
                    return "Rotor {0} had invalid notch of '{1}'".format(
                    rotorName, subelement.text)

            # Invalid element.
            else:
                return "Invalid xml tag '{0}'".format(subelementName)

        return Rotor(rotorName, circuits, notches)


rotorFactory = RotorFactory.Instance()
