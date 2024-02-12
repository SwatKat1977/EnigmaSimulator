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
#ifndef LOGGING_H
#define LOGGING_H
#include <string>

namespace enigmaSimulator {

    enum LogLevel
    {
        kLogLevel_info = 0,
        kLogLevel_trace = 1
    };

    using DebugLoggingCallbackFunc = void (*)(
        std::string functionName, std::string msg, bool clipped);
    using TraceLoggingCallbackFunc = void (*)(
        LogLevel level, std::string msg, bool clipped);

    void AssignLoggingDebugCallback( DebugLoggingCallbackFunc callback );

    void AssignLoggingTraceCallback( TraceLoggingCallbackFunc callback );

    void DebugLog(std::string functionName, const char *format, ...);

    void TraceLog(LogLevel level, const char *format, ...);

#ifdef __OLD__
#ifdef ENIGMASIM_DEBUG
#    define DEBUG_LOG(...) printf (__VA_ARGS__);
#else
#    define DEBUG_LOG(...)
#endif
#endif

}   // namespace enigmaSimulator

#endif  // #ifndef LOGGING_H
