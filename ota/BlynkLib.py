#version=2.0

# The MIT License (MIT)
# Copyright (c) 2015-2018 Volodymyr Shymanskyy
# Copyright (c) 2015 Daniel Campora

"""
	Add support for external socket hook
		+ SIM800L GPRS Networking
		+ A9G
		+ SIM808
"""

import sys;core=sys.modules['Blocky.Core']
from micropython import const
HDR_LEN = const(5)
HDR_FMT = "!BHH"

MAX_MSG_PER_SEC = const(1000)

MSG_RSP = const(0)
MSG_LOGIN = const(2)
MSG_PING  = const(6)
MSG_TWEET = const(12)
MSG_EMAIL = const(13)
MSG_NOTIFY = const(14)
MSG_BRIDGE = const(15)
MSG_HW_SYNC = const(16)
MSG_INTERNAL = const(17)
MSG_PROPERTY = const(19)
MSG_HW = const(20)
MSG_EVENT_LOG = const(64)
MSG_REDIRECT  = const(41)  # TODO: not implemented
MSG_DBG_PRINT  = const(55) # TODO: not implemented
STA_SUCCESS = const(200)
HB_PERIOD = const(10000)
NON_BLK_SOCK = const(0)
MIN_SOCK_TO = const(1) # 1 second
MAX_SOCK_TO = const(5000) # 5 seconds, must be < HB_PERIOD
RECONNECT_DELAY = const(1) # 1 second
TASK_PERIOD_RES = const(50) # 50 ms
IDLE_TIME_MS = const(5) # 5 ms