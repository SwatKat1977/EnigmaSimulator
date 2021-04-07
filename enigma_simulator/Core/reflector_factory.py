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
from Core.json_enabled_class import JsonLoadingClass
from Core.reflector import Reflector
from Core.rotor_contact import RotorContact


# ***********************************************************************
# Singleton class for a factor to create reflectors.
# ***********************************************************************
class ReflectorFactory(JsonLoadingClass):

    BodyElement_Name = 'name'
    BodyElement_Wiring = 'wiring'
    BodyElement_WiringIn = 'in'
    BodyElement_WiringOut = 'out'

    JsonSchema = {
        "definitions":
        {
            "PinWiringEntry":
            {
                "type": "object",
                "additionalProperties" : False,
                "required": [BodyElement_WiringIn, BodyElement_WiringOut],
                "properties":
                {
                    BodyElement_WiringIn: {"type": "string"},
                    BodyElement_WiringOut: {"type": "string"}
                }
            }
        },
        "type" : "object",
        "properties":
        {
            "additionalProperties" : False,
            BodyElement_Name: {"type": "string"},
            BodyElement_Wiring:
            {
                "type" : "array",
                "items": {"$ref": "#/definitions/PinWiringEntry"}
            }
        },
        "required": [BodyElement_Name, BodyElement_Wiring],
        "additionalProperties" : False
    }


    ## Property getter : The last reported error message, blank if none.
    @property
    def last_error_message(self):
        return self._last_error


    def __init__(self):
        self._last_error = ''


    ## Read a reflector JSON file.  If the file is incorrectly formatted or if
    #  there is a validity issue (duplicate wiring) then None is returned
    #  along with lastErrorMessage being set.
    #  @param self The object pointer.
    #  @param xmlFile XML filename string
    #  @param json_file JSON configuration filename
    #  @return Success: Rotor object, failure: None with LastErrorMessage set.
    def build_from_json(self, json_file):

        json_data, err_msg = self.read_json_file(json_file, self.JsonSchema,
                                                 show_validate_error=True)

        if json_data is None:
            self._last_error = err_msg
            return None

        wiring = {}
        wiring_reverse = {}

        for pin in  json_data[self.BodyElement_Wiring]:
            in_pin = RotorContact[pin[self.BodyElement_WiringIn]].value
            out_pin = RotorContact[pin[self.BodyElement_WiringOut]].value

            if in_pin in wiring:
                self._last_error = f"Circuit ({in_pin}:{out_pin}) " + \
                         "input pin is already defined"
                return None

            if out_pin in wiring_reverse:
                self._last_error = f"Circuit ({in_pin}:{out_pin}) " + \
                         "output pin is already defined"
                return None

            wiring[in_pin] = out_pin
            wiring_reverse[out_pin] = in_pin

        # Everything went through successfully, return a built reflector.
        return Reflector(json_data[self.BodyElement_Name], wiring)
