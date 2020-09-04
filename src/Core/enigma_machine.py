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
import os
from Core.enigma_models import ENIGMA_MODELS
from Core.plugboard import Plugboard
from Core.rotor_contact import RotorContact, NO_OF_ROTOR_CONTACTS
from Core.reflector_factory import ReflectorFactory
from Core.rotor_factory import RotorFactory


## Implementation of Enigma machine.
class EnigmaMachine:
    __slots__ = ['_double_step', '_is_configured', '_last_error',
                 '_model_details', '_model_type', '_plugboard',
                 '_reflector', '_rotor_factory', '_reflector_factory',
                 '_rotors', '_display_debug_messages']

    @property
    def configured(self):
        return self._is_configured

    ## Get the instance of the plugboard, it can be None if a plugboard isn't
    #  configured.
    @property
    def last_error(self):
        return self._last_error

    ## Get the instance of the plugboard, it can be None if a plugboard isn't
    #  configured.
    @property
    def plugboard(self):
        return self._plugboard

    ## Get the instance of the reflector.
    @property
    def reflector(self):
        return self._reflector

    ## Flag for displaying additional debug messages.
    @property
    def debug_messages(self):
        return self._display_debug_messages

    @debug_messages.setter
    def debug_messages(self, value):
        self._display_debug_messages = value


    ## Constructor.
    #  plug board => rotors => reflector => rotors => plugboard.
    #  @param self The object pointer.
    #  @param machineSetup Machine setup class
    def __init__(self, model, enable_debugs=False):

        self._model_type = model

        try:
            self._model_details = ENIGMA_MODELS[model]

        except NameError as err:
            print(err)
            raise ValueError('Enigma model is not valid')

        # Flag to enable additional messages so you can see how the Enigma
        # machine should operate.
        self._display_debug_messages = enable_debugs

        # Double-step flag.
        self._double_step = False

        # Last error message.
        self._last_error = None

        # Plugboard object instance.
        self._plugboard = None

        # Reflector object instance.
        self._reflector = None

        # List of rotor instances.
        self._rotors = []

        self._reflector_factory = ReflectorFactory()

        self._rotor_factory = RotorFactory()

        self._is_configured = False


    #  @param self The object pointer.
    def configure_machine(self, rotors, reflector):

        no_of_rotors_req = self._model_details.no_of_rotors.value

        if len(rotors) != no_of_rotors_req:
            self._last_error = 'Invalid number of rotors specified, ' + \
                f'requires {no_of_rotors_req} rotors'
            return False

        rotor_path = '../data/rotors'

        rotor_no = 0
        for rotor_name in rotors:
            rotor_file = f'{self._model_details.short_name}_{rotor_name}.json'
            rotor_file_path = os.path.join(rotor_path, rotor_file)

            rotor = self._rotor_factory.build_from_json(rotor_file_path)

            if rotor is None:
                self._last_error = self._rotor_factory.last_error_message
                return False

            self._rotors.append(rotor)

            rotor_no += 1

        if self._model_details.has_plugboard:
            self._plugboard = Plugboard()

        reflector_path = '../data/reflectors'
        reflector_full = f'{reflector}.json'
        reflector_filename = os.path.join(reflector_path, reflector_full)
        self._reflector = self._reflector_factory.build_from_json(reflector_filename)

        if self._reflector is None:
            self._last_error = self._reflector_factory.last_error_message
            return False

        self._is_configured = True

        return True


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

        self._write_debug_message(f"PressKey received : '{key.name}'")

        #  To encrypt/decrypt a message, we need to run through the circuit:
        # plug board => rotors => reflector => rotors => plugboard.
        #  The variable currentLetter will maintain the contact state.

        rotor_a_value = RotorContact(self._rotors[0].position).name
        rotor_b_value = RotorContact(self._rotors[1].position).name
        rotor_c_value = RotorContact(self._rotors[2].position).name
        self._write_debug_message("Rotors before stepping : " + \
                                  f"{rotor_a_value} | {rotor_b_value}" + \
                                  f" | {rotor_c_value}")

        # Before any en/decoding can begin, rotor turnover should occur.
        self._step_rotors()

        rotor_a_value = RotorContact(self._rotors[0].position).name
        rotor_b_value = RotorContact(self._rotors[1].position).name
        rotor_c_value = RotorContact(self._rotors[2].position).name
        self._write_debug_message("Rotors after stepping : " + \
                                  f"{rotor_a_value} | {rotor_b_value}" + \
                                  f" | {rotor_c_value}")

        # If a plugboard exists for machine then encode through it.
        if self._plugboard != None:
            currentLetter = self._plugboard.get_plug(key)

        # Get the total number of rotors.
        noOfRotors = self._machineSetup.NumberOfRotors

        self._write_debug_message("Passing letter through rotors from right to left")

        # Pass the letter through the rotors from right to left.
        for rotor in reversed(self._rotors):
            self._write_debug_message("Passing '{0}' to {1}",
            RotorContact.Instance().ContactToCharacter(currentLetter), rotor.Name)

            # Get substituted letter from the rotor.  There are two values that
            # are returned.  First is what actual letter came out and then the
            # second that gives you next rotor position after taking the rotors
            # position into account.
            contactNo = rotor.ForwardCircuit(currentLetter)
            self._write_debug_message("'{0}' returned Actual letter of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(contactNo))
            self._write_debug_message("'{0}' returned next rotor position of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(contactNo))
            currentLetter = contactNo

        self._write_debug_message("Passed '{0}' to reflector",
            RotorContact.Instance().ContactToCharacter(currentLetter))

        # Pass the letter through the reflector.
        currentLetter = self._reflector.GetCircuit(currentLetter)
        self._write_debug_message("Reflector returned '{0}'",
            RotorContact.Instance().ContactToCharacter(currentLetter))

        self._write_debug_message("Passing letter through rotors from left to right")

        # Pass the letter through the rotors from left to right.
        for rotor in self._rotors:
            self._write_debug_message("Passing '{0}' to {1}"
                .format(RotorContact.Instance().ContactToCharacter(currentLetter),
                rotor.Name))
            outPin = rotor.ReturnCircuit(currentLetter)
            self._write_debug_message("'{0}' returned Actual letter of '{1}'",
                                      rotor.Name, RotorContact.Instance().ContactToCharacter(outPin))
            currentLetter = outPin

            self._write_debug_message("'{0}' returned next rotor position of '{1}'",
                rotor.Name, RotorContact.Instance().ContactToCharacter(currentLetter))

        # If a plugboard exists for machine then encode through it.
        if self._plugboard != None:
            currentLetter = self._plugboard.GetPlug(currentLetter)

        self._write_debug_message("Output letter '{0}'",
                                  RotorContact.Instance().ContactToCharacter(currentLetter))
        self._write_debug_message(
            "***********************************************************************")

        # Return encoded character.
        return currentLetter


    ##  Rotor stepping occurs from the right to left whilst a stepping notch is
    #   encountered.
    def _step_rotors(self):
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
        willStepNextRotor = rotor.will_step_next()
        rotor.step()

        # If there is a double-step then perform it and reset the flag.
        if self._double_step == True:
            self._rotors[0].Step()
            self._rotors[1].Step()
            self._double_step = False
        
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
            self._double_step = True


    def SetRotorPosition(self, rotorNo, position):
        # Validate rotor positions.
        if position < 1 or position > NO_OF_ROTOR_CONTACTS:
            raise ValueError("Invalid rotor positions")

        if rotorNo < 0 or rotorNo > (len(self._rotors) - 1):
            raise ValueError("Invalid rotor")
       
        # Set the new rotor position.
        self._rotors[rotorNo].position = position


    def _write_debug_message(self, message, *args):
        if self._display_debug_messages is True:
            message = f"[DEBUG] {message}"
            print(message.format(*args))
