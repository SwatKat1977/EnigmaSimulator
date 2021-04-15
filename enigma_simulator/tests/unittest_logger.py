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
import time
import unittest
from simulation.logger import Logger, LogType
import logging

class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }

class UnitTestLogger(unittest.TestCase):
    ''' Unit tests for the Logger class. '''

    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        self._external_msgs = []

    def _external_log_method(self, current_time, log_level, compiled_msg):
        self._external_msgs.append({'time' : current_time, 'level': log_level,
                                     'msg' : compiled_msg})

    def setUp(self):
        self._console_logger = Logger(__name__, write_to_console=True)
        self._mock_hanlder = MockLoggingHandler()
        self._console_logger._logger_instance.addHandler(self._mock_hanlder)

        self._external_logger = Logger('external', write_to_console=False,
                                       external_log_func = self._external_log_method)

    def test_logger_write_to_console(self):
        ''' Logger | Write to console tests '''

        self._console_logger.log_debug('Test debug logging')
        self.assertEqual(self._mock_hanlder.messages.get('debug'), ['Test debug logging'])

        self._console_logger.log_info('Test info logging')
        self.assertEqual(self._mock_hanlder.messages.get('info'), ['Test info logging'])

        self._console_logger.log_error('Test error logging')
        self.assertEqual(self._mock_hanlder.messages.get('error'), ['Test error logging'])

        self._console_logger.log_warn('Test warn logging')
        self.assertEqual(self._mock_hanlder.messages.get('warning'), ['Test warn logging'])

        self._console_logger.log_critical('Test critical logging')
        self.assertEqual(self._mock_hanlder.messages.get('critical'), ['Test critical logging'])

    def test_logger_write_to_file(self):
        ''' Logger | Write to console tests '''

        log_file = f'{round(time.time())}_log.txt'
        file_logger = Logger(__name__, write_to_console=True,
                             log_file = log_file)

        file_logger.log_debug('Test debug logging')
        file_logger.log_info('Test info logging')
        file_logger.log_error('Test error logging')
        file_logger.log_warn('Test warn logging')
        file_logger.log_critical('Test critical logging')

        try:
            with open(log_file, 'r') as handler:
                file_contents = handler.readlines()

        except IOError:
            self.fail('Unable to read log file')

        self.assertEqual(len(file_contents), 5, 'Expected 5 lines')

        # Check each line
        self.assertTrue('Test debug logging' in file_contents[0])
        self.assertTrue('Test info logging' in file_contents[1])
        self.assertTrue('Test error logging' in file_contents[2])
        self.assertTrue('Test warn logging' in file_contents[3])
        self.assertTrue('Test critical logging' in file_contents[4])

    def test_logger_external_log_function(self):
        ''' Logger | External log function tests '''

        self._external_logger.log_debug('Test external debug logging')
        self._external_logger.log_info('Test external info logging')
        self._external_logger.log_error('Test external error logging')
        self._external_logger.log_warn('Test external warn logging')
        self._external_logger.log_critical('Test external critical logging')

        self.assertEqual(len(self._external_msgs), 5, 'Expected 5 lines')

        '''
                self._external_msgs.append({'time' : current_time, 'level': log_level,
                                     'msg' : compiled_msg})
        '''

        # Check each line
        self.assertEqual('Test external debug logging', self._external_msgs[0].get('msg'))
        self.assertEqual(LogType.DEBUG, self._external_msgs[0].get('level'))

        self.assertEqual('Test external info logging', self._external_msgs[1].get('msg'))
        self.assertEqual(LogType.INFO, self._external_msgs[1].get('level'))

        self.assertEqual('Test external error logging', self._external_msgs[2].get('msg'))
        self.assertEqual(LogType.ERROR, self._external_msgs[2].get('level'))

        self.assertEqual('Test external warn logging', self._external_msgs[3].get('msg'))
        self.assertEqual(LogType.WARN, self._external_msgs[3].get('level'))

        self.assertEqual('Test external critical logging', self._external_msgs[4].get('msg'))
        self.assertEqual(LogType.CRITICAL, self._external_msgs[4].get('level'))


if __name__ == '__main__':
    unittest.main()
