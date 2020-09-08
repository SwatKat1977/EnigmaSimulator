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
import unittest
from Core.plugboard import Plugboard
from Core.rotor_contact import RotorContact


# ******************************
# Unit tests for the Rotor class
# ******************************
class UnitTest_Plugboard(unittest.TestCase):

    ##
    # Python unittest setup fixture.
    # Pre-create plugboard for each test.
    # @param self The object pointer.
    def setUp(self):
        self.__plugboard = Plugboard()


    ##
    # Test SetPlug : Invalid source plug ID.
    # SetPlug should raise the exception 'Invalid source plug position'
    # when the plug ID is outside 1 -> 26 (A to Z).
    # @param self The object pointer.
    def test_SetPlug_InvalidPlugSrc(self):

        # Attempt to set a plug with invalid source, it should raise a 
        # ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(0, 12)

        # Verify that the the exception was caught.
        if 'Source plug position not valid' not in str(context.exception):
            self.fail("Did not detect 'Source plug position not valid'")


    ## Test SetPlug : Invalid destination plug ID.
    #  SetPlug should raise the exception 'Invalid destination plug position'
    #  when the plug ID is outside 1 -> 26 (A to Z).
    #  @param self The object pointer.
    def test_SetPlug_InvalidPlugDest(self):

        # Attempt to set a plug with invalid source, it should raise a 
        # ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(RotorContact.B, 27)

        # Verify that the the exception was caught.
        if 'Destination plug position not valid' not in str(context.exception):
            self.fail("Did not detect 'Destination plug position not valid'")


    ##
    # Test SetPlug :  Plug source already in use.
    # SetPlug should raise an exception if the source of plug is  in use.
    # @param self The object pointer.
    def test_SetPlug_PlugSourceInUse(self):

        plugSrc = RotorContact.A
        plugDest = RotorContact.J
        exceptMsg = f'Plugboard source ({plugSrc.name}:{plugDest.name}) is already in use'

        # Set plug to translate 'A' into 'K'.
        self.__plugboard.set_plug(RotorContact.A, RotorContact.K)

        # Attempt to set a plug with an already used source plug, it should
        # raise a ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(plugSrc, plugDest)

        # Verify that the the exception was caught.
        if exceptMsg not in str(context.exception):
            err = f"Did not detect '{exceptMsg}'"
            self.fail(err)


    ##
    # Test SetPlug :  Plug destination already in use.
    # SetPlug should raise an exception if the destination of plug is  in use.
    # @param self The object pointer.
    def test_SetPlug_PlugDestinationInUse(self):

        plug_1_src = RotorContact.Y
        plug_1_dst = RotorContact.B
        plug_2_src = RotorContact.N
        plug_2_dst = RotorContact.B
        exceptMsg = f"Plugboard destination ({plug_2_src.name}:" + \
                    f"{plug_2_dst.name}) is already in use"

        # Set plug to translate 'B' into 'N'.
        self.__plugboard.set_plug(plug_1_src, plug_1_dst)

        # Attempt to set a plug with an already used source plug, it should
        # raise a ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(plug_2_src, plug_2_dst)

        # Verify that the the exception was caught.
        if exceptMsg not in str(context.exception):
            self.fail("Did not detect '{0} | {1}'".format(exceptMsg, context.exception))


    ##
    # Test SetPlug :  Everything OK.
    # SetPlug completed successfully.
    # @param self The object pointer.
    def test_SetPlug_OK(self):

        plugSrc = RotorContact.T
        plugDest = RotorContact.U

        # Set plug to translate 'T' into 'U'.
        self.__plugboard.set_plug(plugSrc, plugDest)


    ##
    # Test GetPlug : Invalid source plug ID.
    # GetPlug should raise the exception 'Invalid source plug position'
    # when the plug ID is outside 1 -> 26 (A to Z).
    # @param self The object pointer.
    def test_GetPlug_InvalidPlugSrc(self):

        # Attempt to set a plug with invalid source, it should raise a 
        # ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.get_plug(0)

        # Verify that the the exception was caught.
        if 'Invalid plug position' not in str(context.exception):
            self.fail("Did not detect 'Invalid source plug position")


    ##
    # Test GetPlug : Source exists in plugs dictionary keys.
    # GetPlug should return valid value as it's been found in the dictionary
    # keys.
    # @param self The object pointer.
    def test_GetPlug_ExistsInDictionaryKeys(self):
        plugSrc = RotorContact.Q
        plugDest = RotorContact.R

        # Set plug to translate 'Q' into 'R'.
        self.__plugboard.set_plug(plugSrc, plugDest)
        self.assertEqual(self.__plugboard.get_plug(plugSrc), plugDest)


    ##
    # Test GetPlug : Source exists in plugs dictionary values.
    # GetPlug should return valid value as it's been found in the dictionary
    # keys.
    # @param self The object pointer.
    def test_GetPlug_ExistsInDictionaryValues(self):
        plugSrc = RotorContact.G
        plugDest = RotorContact.M

        # Set plug to translate 'O' into 'P'.
        self.__plugboard.set_plug(plugSrc, plugDest)
        self.assertEqual(self.__plugboard.get_plug(plugDest), plugSrc)


    ##
    # Test GetPlug : No plug set - pass through.
    # GetPlug should return same as parameter as no plug was inserted.
    # @param self The object pointer.
    def test_GetPlug_Passthrough(self):
        plugSrc = RotorContact.H

        self.assertEqual(self.__plugboard.get_plug(plugSrc), plugSrc)


if __name__ == '__main__':
    unittest.main()
