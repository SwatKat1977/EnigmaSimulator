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
import os
from Core.enigma_models import ENIGMA_MODELS
from Core.plugboard import Plugboard
from Core.rotor_contact import RotorContact, NO_OF_ROTOR_CONTACTS
from Core.reflector_factory import ReflectorFactory
from Core.rotor_factory import RotorFactory


## Implementation of Enigma machine.
class EnigmaMachine:
    # pylint: disable=too-many-instance-attributes

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
    # To encrypt/decrypt a message, we need to run the key through the enigma
    # machine (plug board is optional):
    # plug board => rotors => reflector => rotors => plugboard.
    # @param key Key to encode/decode
    # @return Encoded/decoded character.
    def press_key(self, key):
        self._write_debug_message(f"EnigmaMachine::press_key() received : '{key.name}'")

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
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(key)

        self._write_debug_message("Passing letter through rotors from right to left")

        # Pass the letter through the rotors from right to left.
        for rotor in reversed(self._rotors):
            old_letter = RotorContact(current_letter).name

            # Get substituted letter from the rotor.  There are two values that
            # are returned.  First is what actual letter came out and then the
            # second that gives you next rotor position after taking the rotors
            # position into account.
            current_letter = rotor.get_forward_circuit(current_letter)

            debug_msg = f"Passing '{old_letter}' to {rotor.name} returns " + \
                        f"=> '{RotorContact(current_letter).name}'"
            self._write_debug_message(debug_msg)

        # Pass the letter through the reflector.
        old_letter = RotorContact(current_letter).name
        current_letter = self._reflector.get_circuit(current_letter)

        debug_msg = f"Passed '{old_letter}' to reflector => " + \
                    f"{current_letter.name}"
        self._write_debug_message(debug_msg)

        self._write_debug_message("Passing letter through rotors from left to right")

        # Pass the letter through the rotors from left to right.
        for rotor in self._rotors:
            old_letter = RotorContact(current_letter).name
            current_letter = rotor.get_return_circuit(current_letter)

            debug_msg = f"Passing '{old_letter}' to {rotor.name} =>" + \
                        f"'{RotorContact(current_letter).name}'"
            self._write_debug_message(debug_msg)

        # If a plugboard exists for machine then encode through it.
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(current_letter)

        self._write_debug_message(f"Output letter '{current_letter.name}'")
        self._write_debug_message(
            "***********************************************************************")

        # Return encoded character.
        return current_letter


    def set_rotor_position(self, rotor_no, position):
        # Validate rotor positions.
        if position < 1 or position > NO_OF_ROTOR_CONTACTS:
            raise ValueError("Invalid rotor positions")

        if rotor_no < 0 or rotor_no > (len(self._rotors) - 1):
            raise ValueError("Invalid rotor")

        # Set the new rotor position.
        self._rotors[rotor_no].position = position


    def get_rotor_position(self, rotor_no):
        return self._rotors[rotor_no].position


    ##  Rotor stepping occurs from the right to left whilst a stepping notch is
    #   encountered.
    def _step_rotors(self):
        # Step next rotor flag.
        will_step_next_rotor = False

        ######################################
        ### Assume 3 rotor machine for now ###
        ######################################
        no_of_rotors = 3

        # Determine the furthest right rotor (0 indexed list)
        rotor_position = no_of_rotors -1

        # Because the right-hand pawl has no rotor or ring to its right, rotor
        # stepping happens with every key depression.
        rotor = self._rotors[rotor_position]
        will_step_next_rotor = rotor.will_step_next()
        rotor.step()

        # If there is a double-step then perform it and reset the flag.
        if self._double_step:
            print("[DEBUG] Doing a double step")
            self._rotors[0].step()
            self._rotors[1].step()
            self._double_step = False

        # Only continue if there is more If stepping to be done.
        if not will_step_next_rotor:
            return

        # Move to next rotor.
        rotor_position -= 1
        rotor = self._rotors[rotor_position]

        # Step the next rotor.
        rotor.step()

        # If the 2nd rotor will step rotor 1 (left most one) then a double-step
        # needs to take place.  This is where the middle rotor will step again
        # next button press, along with the left one.
        if rotor.will_step_next():
            self._double_step = True


    def _write_debug_message(self, message, *args):
        if self._display_debug_messages is True:
            message = f"[DEBUG] {message}"
            print(message.format(*args))
