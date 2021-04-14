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
from simulation.enigma_models import ENIGMA_MODELS
from simulation.logger import Logger
from simulation.plugboard import Plugboard
from simulation.reflector import Reflector
from simulation.rotor import Rotor
from simulation.rotor_contact import RotorContact

class Machine:
    ''' Implementation of the Enigma machine mechanics. '''
    # pylint: disable=too-many-instance-attributes

    __slots__ = ['_double_step', '_is_configured', '_last_error', '_logger',
                 '_model_details', '_plugboard', '_reflector', '_rotors']

    @property
    def configured(self):
        return self._is_configured

    @property
    def last_error(self):
        ''' Get the last reported error in human-readable form. '''
        return self._last_error

    @property
    def plugboard(self):
        '''
        Get the instance of the plugboard, it can be None if a plugboard
        isn't configured.
        '''
        return self._plugboard

    @property
    def reflector(self):
        ''' Get the instance of the reflector. '''
        return self._reflector

    def __init__(self):
        self._model_details = None
        self._double_step = False
        self._last_error = ''
        self._plugboard = None
        self._reflector = None
        self._rotors = []
        self._is_configured = False
        self._logger = Logger(__name__, write_to_console = True)

    def configure(self, model : str, rotors, reflector):

        if model not in ENIGMA_MODELS:
            raise ValueError('Enigma model is not valid')

        self._model_details = ENIGMA_MODELS[model]

        self._logger.log_debug(f"Configuring machine as '{model}'")

        no_of_rotors_req = self._model_details.no_of_rotors.value

        if len(rotors) != no_of_rotors_req:
            self._last_error = 'Invalid number of rotors specified, ' + \
                f'requires {no_of_rotors_req} rotors'
            return False

        for rotor in rotors:
            details = [r for r in self._model_details.rotors if r.name == rotor]

            if not details:
                self._last_error = f"Rotor '{rotor}' is invalid, aborting!"
                return False

            details = details[0]
            entry = Rotor(details.name, details.wiring, details.notches,
                          self._logger)
            self._rotors.append(entry)

            self._logger.log_debug(f"Added rotor '{rotor}'")

        if self._model_details.has_plugboard:
            self._logger.log_debug("Machine is using a plugboard")
            self._plugboard = Plugboard()

        details = [r for r in self._model_details.reflectors 
                   if r.name == reflector]

        if not details:
            self._last_error = f"Reflector '{reflector}' is invalid, aborting!"
            return False

        self._logger.log_debug(f"Added reflector '{reflector}'")
        self._reflector = Reflector(details[0].name, details[0].wiring)

        self._is_configured = True

        return True

    def press_key(self, key : RotorContact) -> RotorContact:
        '''
        To encrypt/decrypt a message, we need to run the key through the enigma
        machine in the following order (for some models plugboard is optional):
        plug board => rotors => reflector => rotors => plugboard.
        @param key Key to encode.
        @return Encoded character.
        '''
        self._logger.log_debug(f"Machine::press_key() received : '{key.name}'")

        # To encrypt a key entry it needs to run through the circuit:
        # plug board => rotors => reflector => rotors => plugboard.
        #  The variable currentLetter will maintain the contact state.

        self._log_rotor_states('Rotors before stepping :')

        # Before any encrypting can begin step the rotor.
        self._step_rotors()

        self._log_rotor_states('Rotors after stepping :')

        # If a plugboard exists for machine then encode through it.
        if self._plugboard is not None:
            current_letter = self._plugboard.get_plug(key)
            self._logger.log_debug(f"Plugboard | Passed '{key.name}' in " + \
                                   f"and received '{current_letter.name}'")

        self._logger.log_debug("Passing letter through rotors from right to left")

        # Pass the letter through the rotors from right to left.
        for rotor in reversed(self._rotors):
            old_letter = RotorContact(current_letter).name

            # Get substituted letter from the rotor.  There are two values that
            # are returned.  First is what actual letter came out and then the
            # second that gives you next rotor position after taking the rotors
            # position into account.
            #current_letter = rotor.get_forward_circuit(current_letter)
            current_letter = rotor.encrypt(current_letter)

            debug_msg = f"Rotor | Passing '{old_letter}' to {rotor.name} " + \
                        f"returned '{RotorContact(current_letter).name}'"
            self._logger.log_debug(debug_msg)

        # Pass the letter through the reflector.
        old_letter = RotorContact(current_letter).name
        current_letter = self._reflector.encrypt(current_letter)

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
        ''' Set the position of the rotor. '''

        # Validate rotor positions.
        if position < 0 or position > 25:
            raise ValueError("Invalid rotor positions")

        if rotor_no < 0 or rotor_no > (len(self._rotors) - 1):
            raise ValueError("Invalid rotor")

        # Set the new rotor position.
        self._rotors[rotor_no].position = position

    def get_rotor_position(self, rotor_no):
        return self._rotors[rotor_no].position


    def _step_rotors(self):
        '''
        Rotor stepping occurs from the right to left whilst a stepping
        notch is encountered.
        '''

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

    def _log_rotor_states(self, prefix_str : str) -> None:
        rotor_0 = RotorContact(self._rotors[0].position).name
        rotor_1 = RotorContact(self._rotors[1].position).name
        rotor_2 = RotorContact(self._rotors[2].position).name
        self._logger.log_debug(f"{prefix_str} {rotor_0} | {rotor_1} | " + \
                               f"{rotor_2}")

# 274 #