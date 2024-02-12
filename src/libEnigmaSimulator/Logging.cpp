/*
-----------------------------------------------------------------------------
This source file is part of ITEMS
(Integrated Test Management Suite)
For the latest info, see https://github.com/SwatKat1977/intmac/

Copyright 2014-2023 Integrated Test Management Suite Development Team

    This program is free software : you can redistribute it and /or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https://www.gnu.org/licenses/>.
-----------------------------------------------------------------------------
*/
#include <stdio.h>
#include <iostream>
#include "Logging.h"

namespace enigmaSimulator {

    const int MAX_LOG_MSG_SIZE = 200;

    DebugLoggingCallbackFunc debugLogFunc;
    TraceLoggingCallbackFunc traceLogFunc;

    void AssignLoggingDebugCallback( DebugLoggingCallbackFunc callback )
    {
        debugLogFunc = callback;
    }

    void AssignLoggingTraceCallback( TraceLoggingCallbackFunc callback )
    {
        traceLogFunc = callback;
    }

    void DebugLog(std::string functName, const char *format, ...)
    {
        if (!debugLogFunc) return;

        va_list args;
        va_start(args, format);

        char buffer [MAX_LOG_MSG_SIZE] = "\0";
        int count = vsnprintf ( buffer, MAX_LOG_MSG_SIZE, format, args );
        bool clipped = (count > MAX_LOG_MSG_SIZE);

        va_end(args);

        debugLogFunc(functName, buffer, clipped);
    }

    void TraceLog(LogLevel level, const char *format...)
    {
        if (!traceLogFunc) return;

        va_list args;
        va_start(args, format);

        char buffer [MAX_LOG_MSG_SIZE] = "\0";
        int count = vsnprintf ( buffer, MAX_LOG_MSG_SIZE, format, args );
        bool clipped = (count > MAX_LOG_MSG_SIZE);

        va_end(args);

        traceLogFunc(level, buffer, clipped);
    }

}   // namespace enigmaSimulator
