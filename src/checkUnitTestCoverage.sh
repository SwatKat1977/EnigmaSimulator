rm -rf .coverage
python -m coverage run core_unit_tests.py -v
python -m coverage report -m --omit="Core/unit_tests/rotor.py,core_unit_tests.py,\
    UnitTest_EnigmaMachine.py,Core/unit_tests/rotor_factory.py,\
    UnitTest_MachineConfig.py,Core/unit_tests/plugboard.py,Core/unit_tests/reflector.py,\
    UnitTest_MachineSetup.py,UnitTest_RotorContact.py,Core/unit_tests/reflector_factory.py"
