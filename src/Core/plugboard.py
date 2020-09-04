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
from Core.rotor_contact import NO_OF_ROTOR_CONTACTS


# ***********************************************************************
# Class representing an Enigma plugboard / Steckerbrett (German).
# ***********************************************************************
class Plugboard:

    # Plugboard plug source in use exception message.
    PlugboardSrcInUseMsg = 'Plugboard Source ({0}:{1}) is already in use'

    # Plugboard plug destination in use exception message.
    PlugboardDesInUseMsg = 'Plugboard Destination ({0}:{1}) is already in use'


    ## Class initialisation.
    #  @param self The object pointer.
    def __init__(self):
        self.wiring = {}


    ## Set a plug, giving a source and destination.  Only 1 plug per hole,
    #  or example 2 plugs can't use 'A'. If this, or another exception occurs
    #  then a ValueErrorn exception is generated.
    #  @param self The object pointer.
    #  @param src Source of the plug.
    #  @param src Source of the plug.
    def set_plug(self, src, dest):

        if not (src >= 1) and (src <= NO_OF_ROTOR_CONTACTS):
            raise ValueError("Invalid source plug position")

        if not (dest >= 1) and (dest <= NO_OF_ROTOR_CONTACTS):
            raise ValueError("Invalid destination plug position")

        # Check that source end of the plugboard is not in use.
        if ((src in  self.wiring) or (src in self.wiring.values())):
            raise ValueError(self.PlugboardSrcInUseMsg.format(src, dest))

        # Check that destination end of the plugboard is not in use.
        if ((dest in  self.wiring) or (dest in self.wiring.values())):
            raise ValueError(self.PlugboardDesInUseMsg.format(src, dest))

        self.wiring[src] = dest


    ## Get the other end of a plug.  If there is a plug then work out the other
    #  end, otherwise return same letter.
    #  @param self The object pointer.
    #  @param src Plug to get other end of.
    #  @return Other end of plug.  For example if 'A' is wired to 'T' then 'A'
    #  becomes 'T', but if 'C' isn't wired then it will return 'C'.
    def get_plug(self, src):
        if not (src >= 1) and (src <= NO_OF_ROTOR_CONTACTS):
            raise ValueError("Invalid source plug position")

        # The output of the plug, it will default to pass-through initially.
        plug_output = src

        # Check that the plug is fitted, if it has then modify the outgoing
        # value, otherwise it will pass straight through, e.g. 'T' will remain
        # as 'T'.
        if src in  self.wiring:
            plug_output = self.wiring[src]

        elif src in self.wiring.values():
            plug_output = self.wiring.keys()[self.wiring.values().index(src)]

        return plug_output
