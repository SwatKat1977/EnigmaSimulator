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
import enum
import logging
import logging.config
import time

class LogType(enum.Enum):
    """ Enumeration of log type """

    ## Information that is diagnostically helpful to people more than just
    #  developers (IT, sysadmins, etc.).
    DEBUG = 'debug'

    ## Generally useful information to log (service start/stop, configuration
    #  assumptions, etc). Info I want to always have available but usually
    #  don't care about under normal circumstances.
    INFO = 'info'

    ## Anything that can potentially cause application oddities, but for which
    #  I am automatically recovering. (Such as switching from a primary to
    #  backup server, retrying an operation, missing secondary data, etc.)
    WARN = 'warn'

    ## Any error which is fatal to the operation, but not the service or
    #  application (can't open a required file, missing data, etc.). These
    #  errors will force user (administrator, or direct user) intervention.
    ERROR = 'error'

    ## Any error that is forcing a shutdown of the service or application to
    #  prevent data loss (or further data loss). I reserve these only for the
    #  most heinous errors and situations where there is guaranteed to have
    #  been data corruption or loss.
    CRITICAL = 'critical'

class Logger:
    """ Logger class that can write to a console or an external logger """
    __slots__ = ['_external_logger', '_log_file', '_logger_instance',
                 '_write_to_console']

    def __init__(self, module_name : str, external_log_func = None,
                 write_to_console: bool  = False, log_file=None):
        """
        Logger class constructor.
        @param module_name Name of module associated with logger.
        @param external_log_func External logger method.
        @param write_to_console Boolean flag for writing to console. The
               default value is False.
        @param log_file Namme of of log file (if required). The default value
               is None (don't log to file).
        """
        self._external_logger = external_log_func
        self._log_file = log_file
        self._logger_instance = logging.getLogger(module_name)
        self._write_to_console = write_to_console

        log_format= logging.Formatter("%(asctime)s [%(levelname)s] %(message)s",
                                      "%Y-%m-%d %H:%M:%S")

        console_stream = logging.StreamHandler()
        console_stream.setFormatter(log_format)
        self._logger_instance.setLevel(logging.DEBUG)
        self._logger_instance.addHandler(console_stream)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(log_format)
            self._logger_instance.addHandler(file_handler)

    def log_debug(self, msg, *args) -> None:
        """
        Log a debug level message.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        self._log(LogType.DEBUG, msg, *args)

    def log_error(self, msg, *args) -> None:
        """
        Log an error level message.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        self._log(LogType.ERROR, msg, *args)

    def log_info(self, msg, *args) -> None:
        """
        Log an info level message.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        self._log(LogType.INFO, msg, *args)

    def log_warn(self, msg, *args) -> None:
        """
        Log a warning level message.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        self._log(LogType.WARN, msg, *args)

    def log_critical(self, msg, *args) -> None:
        """
        Log a critical level message.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """
        self._log(LogType.CRITICAL, msg, *args)

    def _log(self, log_level, msg, *args) -> None:
        """
        Log a message using the logger.
        @param log_level Level of the logged message, e.g. debug.
        @param msg Actual message to log.
        @param args Variable arguments used in the message.
        @return None
        """

        if self._write_to_console:
            compiled_msg = msg % args
            method_to_call = getattr(self._logger_instance, log_level.value)
            method_to_call(compiled_msg)

        if self._external_logger:
            current_time = time.time()
            compiled_msg = msg % args
            self._external_logger.add_log_event(current_time, log_level,
                                                compiled_msg)
