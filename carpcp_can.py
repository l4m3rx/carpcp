#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# CAN Message Parse Lib-ish thinggy
#
# TODO: Fix all try/execpt

import re

__name__ = 'carpcp_can'
__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'georgi.kolev[at]gmail.com'

# Expected message syntax:
#  ID		HEX (11bit long value)
#  RTR		Integer (0 or 1)
#  Len		Integer (message len)
#  Data		HEX (Up to 8 bytes)
#
#   ID    RTR       Len        Data
# ID: fff -0- Data: [8] ff ff ff ff ff ff ff ff
# ID: fff -0- Data: [3] ff ff ff
#
# msg_match = r'ID: (\w+) -(\d{1})- Data: \[(\d{1})\] (.+)'
msg_match = r'ID: (\w+) \[(\d{1})\] (.+)'


class CanMsg(object):
    def __init__(self):
        self.mid = 0
        self.rtr = 0
        self.mlen = 0
        self.message = []

    def check_id(self, mid, maxv=0xFFF):
        """ Check message ID integrity """
        if isinstance(mid, int):
            if (mid > 0) and (mid < (maxv + 1)):
                return True
        return False

    def check_msg(self, m):
        """ Check message data integrity """
        try:
            msg = m.split()
            for x in xrange(0, len(msg)):
                msg[x] = int(msg[x], 16)
        except:
            return False
        return msg

    def parse(self, m):
        """ Parse CAN message
            Syntax: ID: (%ARBID) [%LEN] %MESSAGE
            Example: ID: FFF [3] ff ff ff
        """
        matchObj = re.match(msg_match, m, re.I)
        if matchObj:
            match_array = matchObj.groups()
            # Check Message ID
            if self.check_id(int(match_array[0], 16)):
                self.mid = int(match_array[0], 16)
            # Check Message Lenght
            if self.check_id(match_array[1], maxv=7):
                self.mlen = int(match_array[1])
            # Check Message Data
            self.message = self.check_msg(match_array[2])
            # All good?
            if self.mid and self.mlen and self.message:
                return True
        return False

# EOF
