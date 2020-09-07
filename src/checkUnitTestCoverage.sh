rm -rf .coverage
python -m coverage run core_unit_tests.py -v
python -m coverage report -m --omit="UnitTest_Rotor.py,core_unit_tests.py,\
    UnitTest_EnigmaMachine.py,\
    UnitTest_RotorFactory.py,\
    UnitTest_MachineConfig.py,Core/unit_tests/plugboard.py,Core/unit_tests/reflector.py,\
    UnitTest_MachineSetup.py,UnitTest_RotorContact.py,Core/unit_tests/reflectorFactory.py"
