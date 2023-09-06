#!/usr/bin/env python3

import sys
from datetime import datetime
import time
import pytz


FILL_CLOCK_FACE = False


try:
    # if len(sys.argv) < 3:
        # print("Usage: {scriptname} timezone_left timezone_right".format(scriptname=sys.argv[0]), file=sys.stderr)
        # exit(1)

    # try:
        # tzleft  = pytz.timezone(sys.argv[1])
        # tzright = pytz.timezone(sys.argv[2])
    # except pytz.exceptions.UnknownTimeZoneError as e:
        # print('Unknown time zone "{}"'.format(e.args[0]), file=sys.stderr)
        # exit(1)


    hourhands   = ""
    minutehands = ""

    def face_for(t):
        minute = minutehands[ t.minute // 5 ]
        hour   = hourhands  [ t.hour % 12   ]

        if FILL_CLOCK_FACE:
            return "%{O1}%{T8}" + color_for(t) + "%{F#000}"   + hour + minute + "" + "%{T-}%{F}"
        else:
            return "%{O1}%{T8}" + color_for(t) + hour + minute + "%{T-}%{F}"


    def color_for(t):
        if t.hour < 5 or t.hour > 22:
            return "%{F#888888}" # "%{F#888}"
        elif t.hour < 10:
            return "%{F#e2d39a}" # "%{F#DB9}"
        elif t.hour < 14:
            return "%{F#dec7aa}" # "%{F#DDB}"
        elif t.hour < 19:
            return "%{F#deceb0}" # "%{F#DDD}"
        else:
            return "%{F#ff948d}" # "%{F#D9B}"


    while True:
        utcnow   = datetime.now(tz=pytz.utc)
        localnow = datetime.now()
        # leftnow  = utcnow.astimezone(tzleft )
        # rightnow = utcnow.astimezone(tzright)

        localcolor = color_for(localnow)

        khal_link = lambda x: "%{A1:i3-sensible-terminal -x khal interactive &:}" + x + "%{A}"
        clock_link = lambda x, args: "%{A1:i3-sensible-terminal -x tty-clock -cC3 " + args + " &:}" + x + "%{A}"

        print(
            khal_link(
                localcolor +
                localnow.strftime("%A") +
                "%{F}     "
            ) +

            # face_for(leftnow) +

            clock_link("     %{T4}" + localcolor + localnow.strftime("%H") + "%{F}", "") +
            clock_link("%{O2}%{T8}" +              face_for(localnow), "-D") +
            clock_link("%{O2}%{T4}" + localcolor + localnow.strftime("%M") + "%{T-}%{F}     ", "-s") +

            # face_for(rightnow) + " " +

            khal_link(
                "    " +
                localcolor +
                localnow.strftime("%d %b") +
                "%{F}"
            ),

            flush = True
        )

        delay = 60 - localnow.second - (localnow.microsecond * 10e-7)
        time.sleep(delay)

except Exception as e:
    print(e, file=sys.stderr)
