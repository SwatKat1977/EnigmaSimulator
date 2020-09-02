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
from Rotor import *
from RotorContact import RotorContact


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
    def LastErrorMessage(self):
        return self._lastErrorMsg


    def __init__(self):
        self._lastErrorMsg = ''


    ## Read a rotor JSON file.  If the file is incorrectly formatted or if
    #  there is a validity issue (duplicate wiring) then None is returned
    #  along with lastErrorMessage being set.
    #  @param self The object pointer
    #  @param jsonFile JSON configuration filename
    # @return Success: Rotor object, failure: None with LastErrorMessage set.
    def BuildFromJson(self, jsonFile):

        try:
            with open(jsonFile) as fileHandle:
                fileContents = fileHandle.read()

        except IOError as excpt:
            self._lastErrorMsg = "Unable to open configuration file '" + \
                f"{jsonFile}', reason: {excpt.strerror}"
            return None

        try:
            rotorJson = json.loads(fileContents)

        except json.JSONDecodeError as excpt:
            self._lastErrorMsg = "Unable to parse configuration file" + \
                f"{jsonFile}, reason: {excpt}"
            return None

        try:
            jsonschema.validate(instance=rotorJson,
                                schema=self._JsonSchema)

        except jsonschema.exceptions.ValidationError as ex:
            self.__lastErrorMsg = f"Configuration file {jsonFile} failed " + \
                "to validate against expected schema.  Please check!.  "+ \
                f"Msg: {ex}"
            return None

        wiring = {}
        wiringReverse = {}

        turnoverNotches = []

        for notch in rotorJson[self._BodyElement_Notches]:
            turnoverNotches.append(notch)

        for pin in  rotorJson[self._BodyElement_Wiring]:
            inPin = pin[self._BodyElement_WiringIn]
            outPin = pin[self._BodyElement_WiringOut]
            if inPin in wiring:
                self._lastErrorMsg = f"Circuit {inPin}:{outPin}) input " + \
                         "pin is already defined"

            if outPin in wiringReverse:
                self._lastErrorMsg = f"Circuit {inPin}:{outPin}) output " + \
                         "pin is already defined"

            wiring[inPin] = outPin
            wiringReverse = inPin

        # Everything went through successfully, return rotor.
        return Rotor(rotorJson[self._BodyElement_Name], wiring, turnoverNotches)


rotorFactory = RotorFactory()
r = rotorFactory.BuildFromJson('../data/rotors/Enigma1_I.json')
if r is None:
    print(rotorFactory.LastErrorMessage)
