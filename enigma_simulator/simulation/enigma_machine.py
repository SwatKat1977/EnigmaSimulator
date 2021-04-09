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
import os
from simulation.enigma_models import ENIGMA_MODELS
from simulation.logger import Logger
from simulation.plugboard import Plugboard
from simulation.rotor import Rotor
from simulation.rotor_contact import RotorContact
from simulation.reflector_factory import ReflectorFactory

class EnigmaMachine:
    ''' Implementation of Enigma machine. '''
    # pylint: disable=too-many-instance-attributes

    __slots__ = ['_double_step', '_is_configured', '_last_error',
                 '_logger', '_model_details', '_model_type', '_plugboard',
                 '_reflector', '_reflector_factory', '_rotors']

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

    ## Constructor.
    #  plug board => rotors => reflector => rotors => plugboard.
    #  @param self The object pointer.
    #  @param machineSetup Machine setup class
    def __init__(self, model, message_handler=None):

        self._model_type = model

        if model not in ENIGMA_MODELS:
            raise ValueError('Enigma model is not valid')

        self._model_details = ENIGMA_MODELS[model]

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

        self._is_configured = False

        self._logger = Logger(__name__, write_to_console = True)

    #  @param self The object pointer.
    def configure_machine(self, rotors, reflector):

        no_of_rotors_req = self._model_details.no_of_rotors.value

        if len(rotors) != no_of_rotors_req:
            self._last_error = 'Invalid number of rotors specified, ' + \
                f'requires {no_of_rotors_req} rotors'
            return False

        for rotor in rotors:
            details = [r for r in self._model_details.rotors if r.name == rotor]

            if not details:
                self._last_error = f'Rotor {rotor} is invalid, aborting!'
                return False

            details = details[0]
            entry = Rotor(details.name, details.wiring, details.notches,
                          self._logger)
            self._rotors.append(entry)

        if self._model_details.has_plugboard:
            self._plugboard = Plugboard()

        reflector_path = '../data/reflectors'
        reflector_full = f'{reflector}.json'
        reflector_filename = os.path.join(reflector_path, reflector_full)
        self._reflector = self._reflector_factory.build_from_json(reflector_filename)

        if self._reflector is None:
            self._last_error = f"Reflector read failure | " + \
                               self._reflector_factory.last_error_message
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
        self._logger.log_debug(
            f"EnigmaMachine::press_key() received : '{key.name}'")

        #  To encrypt/decrypt a message, we need to run through the circuit:
        # plug board => rotors => reflector => rotors => plugboard.
        #  The variable currentLetter will maintain the contact state.

        rotor_a_value = RotorContact(self._rotors[0].position).name
        rotor_b_value = RotorContact(self._rotors[1].position).name
        rotor_c_value = RotorContact(self._rotors[2].position).name

        self._logger.log_debug("Rotors before stepping : " + \
            f"{rotor_a_value} | {rotor_b_value} | {rotor_c_value}")

        # Before any en/decoding can begin, rotor turnover should occur.
        self._step_rotors()

        rotor_a_value = RotorContact(self._rotors[0].position).name
        rotor_b_value = RotorContact(self._rotors[1].position).name
        rotor_c_value = RotorContact(self._rotors[2].position).name

        self._logger.log_debug("Rotors after stepping : " + \
            f"{rotor_a_value} | {rotor_b_value} | {rotor_c_value}")

        # If a plugboard exists for machine then encode through it.
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(key)

        self._logger.log_debug("Passing letter through rotors from right to left")

        # Pass the letter through the rotors from right to left.
        for rotor in reversed(self._rotors):
            old_letter = RotorContact(current_letter).name

            print(rotor.name)
            # Get substituted letter from the rotor.  There are two values that
            # are returned.  First is what actual letter came out and then the
            # second that gives you next rotor position after taking the rotors
            # position into account.
            #current_letter = rotor.get_forward_circuit(current_letter)
            current_letter = rotor.encrypt(current_letter)

            debug_msg = f"Passing '{old_letter}' to {rotor.name} returns " + \
                        f"=> '{RotorContact(current_letter).name}'"
            self._logger.log_debug(debug_msg)

        # Pass the letter through the reflector.
        old_letter = RotorContact(current_letter).name
        current_letter = self._reflector.get_circuit(current_letter)

        debug_msg = f"Passed '{old_letter}' to reflector => " + \
                    f"{current_letter.name}"
        self._logger.log_debug(debug_msg)

        self._logger.log_debug("Passing letter through rotors from left to right")

        # Pass the letter through the rotors from left to right.
        for rotor in self._rotors:
            old_letter = RotorContact(current_letter).name
            current_letter = rotor.encrypt(current_letter, forward=False)

            debug_msg = f"Passing '{old_letter}' to {rotor.name} =>" + \
                        f"'{RotorContact(current_letter).name}'"
            self._logger.log_debug(debug_msg)

        # If a plugboard exists for machine then encode through it.
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(current_letter)

        self._logger.log_debug(f"Output letter '{current_letter.name}'")
        self._logger.log_debug("*********************************************")

        # Return encoded character.
        return current_letter


    def set_rotor_position(self, rotor_no, position):
        # Validate rotor positions.
        if position < 0 or position > 25:
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
