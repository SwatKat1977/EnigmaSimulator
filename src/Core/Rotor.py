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
from RotorContact import RotorContact


# ***********************************************************************
# Class representing an Enigma rotor / wheel /drum / Walzen (German).
# ***********************************************************************
class Rotor(object):

    ##
    # Property getter 'Name' : Name of the rotor.
    @property
    def Name(self):
        return self.__name

    ##
    # Property getter 'Wiring' : How the rotor is wired.
    @property
    def Wiring(self):
        return self.__wiring

    ##
    # Property getter 'NotchLocations' : Location of the turnover notch(es).
    @property
    def NotchLocations(self):
        return self.__notchLocations

    ##
    # Property getter 'Position' : Position of the notches.
    @property
    def Position(self):
        return self.__position

    @Position.setter
    def Position(self, value):
        # Validate rotor positions.
        if value < 1 or value > RotorContact.Instance().NUMBER_OF_CONTACTS:
            raise ValueError("Invalid rotor positions")

        # Set the position.
        self.__position = value

    ##
    # Property getter 'RingSetting' : Ring setting of the rotor.
    @property
    def RingSetting(self):
        return self.__ringSetting

    @RingSetting.setter
    def RingSetting(self, value):
        # Validate ring position.
        if value < 1 or value > RotorContact.Instance().NUMBER_OF_CONTACTS:
            raise ValueError("Invalid ring positions")

        # Set the ring position.
        self.__ringSetting = value


    ##
    # Constructor.. Wiring is from right => left
    # messages that is being handled.
    # @param self The object pointer.
    # @param name Human readable rotor name.
    # @param wiring Wiring setting from right to left.
    # @param notchLocations Location of the turnover notches.
    def __init__(self, name, wiring, notchLocations):
        # Name of the rotor (e.g. Rotor I).
        self.__name = name

        # Location of the turnover notch(es).
        self.__notchLocations = notchLocations

        # Current position of the rotor.
        self.__position = 1

        # Ring setting (Ringstellung) for the rotor
        self.__ringSetting = 1

        # Check to make sure wiring is a list.
        if not isinstance(wiring, (dict)):
            raise ValueError("Incompatible rotor wiring diagram")

        if len(wiring) != RotorContact.Instance().NUMBER_OF_CONTACTS:
            raise ValueError("Incomplete wiring diagram")

        # define how the rotor is internally wired.
        self.__wiring = wiring


    ##
    # Step the rotor.
    # @param self The object pointer.
    def Step(self):
        if self.__position == RotorContact.Instance().NUMBER_OF_CONTACTS:
            self.__position = 1
        else:
            self.__position += 1


    ##
    # Get the output (circuit) using the contacts on the right-hand side or the
    # contacts on the left hand side of the rotor.
    # @param self The object pointer.
    # @param contact Reference contact to get circuit with.
    # @return A contact number.
    def ForwardCircuit(self, contact):
        # Determine which contact number taking position into account.  If it
        # has 'wrapped' around then work out new contact based on it.
        inContact = (contact + self.__position) -1
        if inContact > RotorContact.Instance().NUMBER_OF_CONTACTS:
            inContact = inContact\
                - RotorContact.Instance().NUMBER_OF_CONTACTS

        # Wiring circuit in forward direction
        outContact = self.__wiring[inContact]

        '''
        # Ring settings are not implemented - untested code
        if self.__ringSetting > 1:
            #outputPin = outputPin + (self.__ringSetting -1)

            if (outputPin - (self.__ringSetting -1)) <= 0:
                outputPin = NumberOfRotorPins - ((self.__ringSetting -1) \
                 - outputPin)
            else:
                outputPin -= (self.__ringSetting -1)

            #if outputPin > NumberOfRotorPins:
            #    outputPin = outputPin - NumberOfRotorPins;
        '''

        offsettedContact = outContact

        # If there is a rotor offset present we need to adjust the out contact
        # so it's taken into account.
        if self.Position > 1:
            # If the contact position has wrapped after taking the offset into
            # account we need to correct it.
            if (outContact - (self.Position -1)) <= 0:
                offsettedContact = RotorContact.Instance().NUMBER_OF_CONTACTS\
                    - ((self.Position -1) - outContact)

            else:
                offsettedContact -= (self.Position -1)

        return offsettedContact


    ##
    # Get the output (circuit) from the return route using the contacts as a
    # reference.
    # @param self The object pointer.
    # @param contact Reference contact to get circuit with.
    # @return The contact number.
    def ReturnCircuit(self, contact):
        # Determine contact number with position taken into account.
        inContact = contact + (self.__position -1)
        if inContact > RotorContact.Instance().NUMBER_OF_CONTACTS:
            inContact = inContact - RotorContact.Instance().NUMBER_OF_CONTACTS;

        # Get the outgoing contact number using a reverse dictionary lookup.
        outContact = self.__wiring.keys()[self.__wiring.values().index(inContact)]

        '''
        if self.__ringSetting > 0:
            if (outputPin - (self.__ringSetting -1)) <= 0:
                outputPin = NumberOfRotorPins - ((self.__ringSetting -1) \
                 - outputPin)
            else:
                outputPin -= (self.__ringSetting -1)
        '''
        
        '''
        # Ring settings are not implemented - untested code
        if self.__ringSetting > 1:
            op = outputPin
            outputPin = outputPin + (self.__ringSetting -1)
            print("[DEBUG] Pin after ring offset : '{0}' [{1}] returns '{2}' [{3}]"
            .format(RotorContacts[outputPin], outputPin,
             RotorContacts[outputPin], outputPin))

            print("[DEBUG] OutputPin = pin ({0}) + ring ({1}) -1 == {2}"
            .format(op, self.__ringSetting, outputPin))

            if outputPin > NumberOfRotorPins:
                outputPin = outputPin - NumberOfRotorPins;
        '''

        # If there is a rotor offset present we need to adjust the out contact
        # so it's taken into account.
        if (self.Position -1) > 0:
            if (outContact - (self.Position -1)) <= 0:
                outContact = RotorContact.Instance().NUMBER_OF_CONTACTS\
                    - ((self.Position -1) - outContact)
            else:
                outContact -= (self.Position -1)

        return outContact


    ##
    # Check to see if the rotor will cause the next one to also step.
    # @param self The object pointer.
    # @return True if when this steps it will cause the next to to, otherwise
    # False is returned.
    def WillStepNext(self):
        return self.__position in self.__notchLocations
