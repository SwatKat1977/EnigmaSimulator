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
from tests.enigma_machine import UnitTest_EnigmaMachine
#from UnitTest_MachineSetup import UnitTest_MachineSetup
from tests.reflector import UnitTest_Reflector
from tests.plugboard import UnitTest_Plugboard
from tests.reflector_factory import UnitTest_ReflectorFactory
from tests.rotor import UnitTest_Rotor

if __name__ == '__main__':
    unittest.main()
