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
from enum import Enum
from Core.rotor_contact import RotorContact
from Core.reflector_factory import ReflectorFactory


## Enumeration referring to a rotor within the machine.  One is far left.
class RotorPosition(Enum):
    One = 0
    Two = 1
    Three = 2
    Four = 3


## Implementation of Enigma machine.
class EnigmaMachine:

    ##
    # Get the instance of the plugboard, it can be None if a plugboard isn't
    # configured.
    @property
    def Plugboard(self):
        return self._plugboard

    ##
    # Get the instance of the reflector.
    @property
    def Reflector(self):
        return self._reflector

    ##
    # Get the trace route flag.
    @property
    def Trace(self):
        return self._traceRoute

    @Trace.setter
    def Trace(self, value):
        self._traceRoute = value


    ##
    # Constructor.
    # plug board => rotors => reflector => rotors => plugboard.
    # @param machineSetup Machine setup class
    def __init__(self, machineSetup, rotors, reflector, trace = False):

        # Flag to enable additional messages so you can see how the Enigma
        # machine should operate.
        self._traceRoute = trace

        # Machine setup instance.
        self._machineSetup = machineSetup

        # Reflector object instance.
        self._reflector = reflector

        # Plugboard object instance.
        self._plugboard = machineSetup.Plugboard

        # List of rotor instances. 
        self._rotors = []

        # Double-step flag.
        self._doubleStep = False

        # Take the rotor name and convert it into a rotor instance.
        for rotor in machineSetup.Rotors:
            if rotor not in rotors:
                raise ValueError("Invalid rotor name '{0}'!".format(rotor))

            # Add the rotor to the list.
            self._rotors.append(rotors[rotor])


    ##
    # Get a rotor instance from the Enigma machine.
    # @param rotorNo Rotor to retrieve.
    # @return Returns rotor instance or ValueError exception if an invalid
    # rotor is passed in.
    def GetRotor(self, rotorNo):
        # Verify that the rotor number passed in is valid.
        if rotorNo < 0 or rotorNo > len(self._rotors):
            raise ValueError('Incorrect rotor number.')

        return self._rotors[rotorNo]


    ##
    # To encrypt/decrypt a message, we need to run the key through the enigma
    # machine (plug board is optional):
    # plug board => rotors => reflector => rotors => plugboard.
    # @param key Key to encode/decode
    # @return Encoded/decoded character.
    def PressKey(self, key):
        currentLetter = key
        self.Traceroute('PressKey received : {0} ({1})'.format(key,
            RotorContact.Instance().ContactToCharacter(key)))

        #  To encrypt/decrypt a message, we need to run through the circuit:
        # plug board => rotors => reflector => rotors => plugboard.
        #  The variable currentLetter will maintain the contact state.

        self.Traceroute("Rotors before stepping : {0} | {1} | {2}",
            RotorContact.Instance().ContactToCharacter(self._rotors[0].Position),
            RotorContact.Instance().ContactToCharacter(self._rotors[1].Position),
            RotorContact.Instance().ContactToCharacter(self._rotors[2].Position))

        # Before any en/decoding can begin, rotor turnover should occur.
        self._StepRotors()

        self.Traceroute("Rotors after stepping : {0} | {1} | {2}",
            RotorContact.Instance().ContactToCharacter(self._rotors[0].Position),
            RotorContact.Instance().ContactToCharacter(self._rotors[1].Position),
            RotorContact.Instance().ContactToCharacter(self._rotors[2].Position))

        # If a plugboard exists for machine then encode through it.
        if self._plugboard != None:
            currentLetter = self._plugboard.GetPlug(key)

        # Get the total number of rotors.
        noOfRotors = self._machineSetup.NumberOfRotors

        self.Traceroute("Passing letter through rotors from right to left")

        # Pass the letter through the rotors from right to left.
        for rotor in reversed(self._rotors):
            self.Traceroute("Passing '{0}' to {1}",
            RotorContact.Instance().ContactToCharacter(currentLetter), rotor.Name)

            # Get substituted letter from the rotor.  There are two values that
            # are returned.  First is what actual letter came out and then the
            # second that gives you next rotor position after taking the rotors
            # position into account.
            contactNo = rotor.ForwardCircuit(currentLetter)
            self.Traceroute("'{0}' returned Actual letter of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(contactNo))
            self.Traceroute("'{0}' returned next rotor position of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(contactNo))
            currentLetter = contactNo

        self.Traceroute("Passed '{0}' to reflector",
            RotorContact.Instance().ContactToCharacter(currentLetter))

        # Pass the letter through the reflector.
        currentLetter = self._reflector.GetCircuit(currentLetter)
        self.Traceroute("Reflector returned '{0}'",
            RotorContact.Instance().ContactToCharacter(currentLetter))

        self.Traceroute("Passing letter through rotors from left to right")

        # Pass the letter through the rotors from left to right.
        for rotor in self._rotors:
            self.Traceroute("Passing '{0}' to {1}"
                .format(RotorContact.Instance().ContactToCharacter(currentLetter),
                rotor.Name))
            outPin = rotor.ReturnCircuit(currentLetter)
            self.Traceroute("'{0}' returned Actual letter of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(outPin))
            currentLetter = outPin

            self.Traceroute("'{0}' returned next rotor position of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(currentLetter))

        # If a plugboard exists for machine then encode through it.
        if self._plugboard != None:
            currentLetter = self._plugboard.GetPlug(currentLetter)

        self.Traceroute("Output letter '{0}'",
                        RotorContact.Instance().ContactToCharacter(currentLetter))
        self.Traceroute(
            "***********************************************************************")

        # Return encoded character.
        return currentLetter


    ##    
    # Rotor stepping occurs from the right to left whilst a stepping notch is
    # encountered.
    def _StepRotors(self):
        # Step next rotor flag.
        willStepNextRotor = False
        
        ######################################
        ### Assume 3 rotor machine for now ###
        ######################################
        numberOfRotors = 3

        # Determine the furthest right rotor (0 indexed list)
        rotorPosition = numberOfRotors -1

        # Because the right-hand pawl has no rotor or ring to its right, rotor
        # stepping happens with every key depression.
        rotor = self._rotors[rotorPosition]
        willStepNextRotor = rotor.WillStepNext()
        rotor.Step()

        # If there is a double-step then perform it and reset the flag.
        if self._doubleStep == True:
            self._rotors[0].Step()
            self._rotors[1].Step()
            self._doubleStep = False
        
        # Only continue if there is more If stepping to be done.
        if willStepNextRotor == False:
            return

        # Move to next rotor.
        rotorPosition -= 1
        rotor = self._rotors[rotorPosition]

        # Step the next rotor.
        rotor.Step()

        # If the 2nd rotor will step rotor 1 (left most one) then a double-step
        # needs to take place.  This is where the middle rotor will step again
        # next button press, along with the left one.
        if rotor.WillStepNext() == True:
            self._doubleStep = True


    def SetRotorPosition(self, rotorNo, position):
        # Validate rotor positions.
        if position < 1 or position > RotorContact.Instance().NUMBER_OF_CONTACTS:
            raise ValueError("Invalid rotor positions")

        if rotorNo < 0 or rotorNo > (len(self._rotors) - 1):
            raise ValueError("Invalid rotor")
            
        # Set the new rotor position.
        self._rotors[rotorNo].Position = position


    def Traceroute(self, message, *args):
        if self._traceRoute == True:
            message = "[TRACE] {0}".format(message)
            print(message.format(*args))
