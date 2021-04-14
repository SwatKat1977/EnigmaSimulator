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
import unittest
from simulation.plugboard import Plugboard
from simulation.rotor_contact import RotorContact

class UnitTestPlugboard(unittest.TestCase):
    ''' Unit tests for the Rotor class '''

    def setUp(self):
        self.__plugboard = Plugboard()

    def test_SetPlug_InvalidPlugSrc(self):
        '''
        Test Invalid source plug ID. SetPlug() should raise the
        exception 'Source plug position not valid' when a plug is not a
        RotorContact.
        '''

        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug('a rotor', 12)

        if 'Source plug position not valid' not in str(context.exception):
            self.fail("Did not detect 'Source plug position not valid'")

    def test_SetPlug_InvalidPlugDest(self):
        '''
        Test Invalid destination plug ID. SetPlug() should raise the exception
        'Invalid destination plug position' when a plug is not a RotorContact.
        '''

        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(RotorContact.B, 27)

        if 'Destination plug position not valid' not in str(context.exception):
            self.fail("Did not detect 'Destination plug position not valid'")

    def test_SetPlug_PlugSourceInUse(self):
        '''
        Test that plug source already in use. SetPlug should raise an exception
        if the source of plug is  in use.
        '''
        plug_src = RotorContact.A
        plug_dest = RotorContact.J
        except_msg = f'Plugboard source ({plug_src.name}:{plug_dest.name}) is already used'

        # Set plug to translate 'A' into 'K'.
        self.__plugboard.set_plug(RotorContact.A, RotorContact.K)

        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(plug_src, plug_dest)

        if except_msg not in str(context.exception):
            err = f"Did not detect '{except_msg}'"
            print(context.exception)
            self.fail(err)

    def test_SetPlug_PlugDestinationInUse(self):
        '''
        # Test SetPlug :  Plug destination already in use.
        # SetPlug should raise an exception if the destination of plug is  in use.
        # @param self The object pointer.
        '''
        
        plug_1_src = RotorContact.Y
        plug_1_dst = RotorContact.B
        plug_2_src = RotorContact.N
        plug_2_dst = RotorContact.B
        except_msg = f"Plugboard destination ({plug_2_src.name}:" + \
                     f"{plug_2_dst.name}) is already in use"

        # Set plug to translate 'B' into 'N'.
        self.__plugboard.set_plug(plug_1_src, plug_1_dst)

        # Attempt to set a plug with an already used source plug, it should
        # raise a ValueError exception.
        with self.assertRaises(ValueError) as context:
            self.__plugboard.set_plug(plug_2_src, plug_2_dst)

        # Verify that the the exception was caught.
        if except_msg not in str(context.exception):
            self.fail(f"Did not detect '{except_msg} | {context.exception}'")

    def test_get_plug_invalid_plug_source(self):
        '''
        Test GetPlug() Invalid source plug ID. The exception 'Invalid source
        # be raised if the parameter is not of type RotorPosition.
        '''

        with self.assertRaises(ValueError) as context:
            self.__plugboard.get_plug(0)

        if 'Invalid plug position' not in str(context.exception):
            self.fail("Did not detect 'Invalid source plug position")

    def test_get_plug_source_plug_has_been_set(self):
        '''
        Test GetPlug() : Source plug has been set, which is what is returned.
        '''
        plug_src = RotorContact.Q
        plug_dest = RotorContact.R

        # Set plug to translate 'Q' into 'R'.
        self.__plugboard.set_plug(plug_src, plug_dest)
        self.assertEqual(self.__plugboard.get_plug(plug_src), plug_dest)

    def test_get_plug_destination_plug_has_been_set(self):
        '''
        Test GetPlug() : Destination plug has been set, which is returned.
        '''
        plug_src = RotorContact.G
        plug_dest = RotorContact.M

        # Set plug to translate 'O' into 'P'.
        self.__plugboard.set_plug(plug_src, plug_dest)
        self.assertEqual(self.__plugboard.get_plug(plug_dest), plug_src)

    def test_GetPlug_Passthrough(self):
        '''
        Test GetPlug() when no plug set pass through is used. GetPlug() should
        return the same contact as the parameter as no plug was inserted.
        '''
        plug_src = RotorContact.H

        self.assertEqual(self.__plugboard.get_plug(plug_src), plug_src)

if __name__ == '__main__':
    unittest.main()
