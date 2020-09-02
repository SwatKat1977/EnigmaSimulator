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
import json
import jsonschema
from rotor import Rotor
from rotor_contact import RotorContact


class RotorFactory:

    slots = ['_BodyElement_Notches', '_BodyElement_Wiring',
             '_BodyElement_WiringIn', '_BodyElement_WiringOut',
             '_JsonSchema']

    _BodyElement_Name = 'name'
    _BodyElement_Notches = 'notches'
    _BodyElement_Wiring = 'wiring'
    _BodyElement_WiringIn = 'in'
    _BodyElement_WiringOut = 'out'

    _JsonSchema = {
        "definitions":
        {
            "PinWiringEntry":
            {
                "type": "object",
                "additionalProperties" : False,
                "required": [_BodyElement_WiringIn, _BodyElement_WiringOut],
                "properties":
                {
                    _BodyElement_WiringIn: {"type": "string"},
                    _BodyElement_WiringOut: {"type": "string"}
                }
            }
        },
        "type" : "object",
        "properties":
        {
            "additionalProperties" : False,
            _BodyElement_Name: {"type": "string"},
            _BodyElement_Notches:
            {
                "type": "array",
                "items": {"type": "string"}
            },
            _BodyElement_Wiring:
            {
                "type" : "array",
                "items": {"$ref": "#/definitions/PinWiringEntry"}
            }
        },
        "required": [_BodyElement_Name, _BodyElement_Notches,
                     _BodyElement_Wiring],
        "additionalProperties" : False
    }

    ## Property getter : The last reported error message, blank if none.
    @property
    def last_error_message(self):
        return self.last_error_msg


    def __init__(self):
        self.last_error_msg = ''


    ## Read a rotor JSON file.  If the file is incorrectly formatted or if
    #  there is a validity issue (duplicate wiring) then None is returned
    #  along with lastErrorMessage being set.
    #  @param self The object pointer
    #  @param json_file JSON configuration filename
    # @return Success: Rotor object, failure: None with LastErrorMessage set.
    def build_from_json(self, json_file):

        try:
            with open(json_file) as file_handle:
                file_contents = file_handle.read()

        except IOError as excpt:
            self.last_error_msg = "Unable to open rotor file '" + \
                f"{json_file}', reason: {excpt.strerror}"
            return None

        try:
            rotor_json = json.loads(file_contents)

        except json.JSONDecodeError as excpt:
            self.last_error_msg = "Unable to parse rotor file" + \
                f"{json_file}, reason: {excpt}"
            return None

        try:
            jsonschema.validate(instance=rotor_json,
                                schema=self._JsonSchema)

        except jsonschema.exceptions.ValidationError as ex:
            self.last_error_msg = f"Rotor file {json_file} failed " + \
                "to validate against expected schema.  Please check!.  "+ \
                f"Msg: {ex}"
            return None

        wiring = {}
        wiring_reverse = {}
        turnover_notches = []

        for notch in rotor_json[self._BodyElement_Notches]:
            turnover_notches.append(notch)

        for pin in  rotor_json[self._BodyElement_Wiring]:
            in_pin = pin[self._BodyElement_WiringIn]
            out_pin = pin[self._BodyElement_WiringOut]
            if in_pin in wiring:
                self.last_error_msg = f"Circuit {in_pin}:{out_pin}) " + \
                         "input pin is already defined"

            if out_pin in wiring_reverse:
                self.last_error_msg = f"Circuit {in_pin}:{out_pin}) " + \
                         "output pin is already defined"

            wiring[RotorContact[in_pin]] = RotorContact[out_pin]
            wiring_reverse[RotorContact[out_pin]] = RotorContact[in_pin]

        # Everything went through successfully, return rotor.
        return Rotor(rotor_json[self._BodyElement_Name], wiring,
                     turnover_notches)


FACTORY = RotorFactory()
ROTOR = FACTORY.build_from_json('../data/rotors/Enigma1_I.json')
if ROTOR is None:
    print(FACTORY.last_error_message)
else:
    print(ROTOR)
