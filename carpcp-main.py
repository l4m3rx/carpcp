#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'georgi.kolev_[at]_gmail.com'
__name__ = 'carpcp-main'

import logging
from time import sleep
from serial import Serial
from thread import start_new_thread

import carpcp_conf as conf
import carpcp_lib as carlib
from carpcp_can import CanMsg
from carpcp_bmw import CarStatus
try:
    from procname import setprocname
    setprocname(__name__)
except:
    print('Warning: "import procname" failed :(')
    print('Warning: Skipping process rename!')


def ser2sock(serial_dev, mcast_sock, car_status, can_msg, logger):
    """ serial-to-socket thread """
    counter = 0
    while 42:
        buffer = serial_dev.readline()
        if can_msg.parse(buffer.strip()):
            results = car_status.msg(can_msg)
            if results:
                counter += 1
                for result in results:
                    if result:
                        carlib.mcast_send(mcast_sock, result)
                        logger.debug('%s' % result)
            # We should resend some stuff from time to time
            if counter == 1024:
                for data in car_status.schedule():
                    carlib.mcast_send(mcast_sock, data)
                counter = 0


if __name__ == '__main__':
    # Setup logging
    logger = logging.getLogger(__name__)
    logger.setLevel(conf.LOG_LEVEL)
    logf = logging.FileHandler(conf.LOG_FILE)
    # logf = logging.StreamHandler()
    logf.setLevel(conf.LOG_LEVEL)
    formatter = logging.Formatter(conf.LOG_FORMAT)
    logf.setFormatter(formatter)
    logger.addHandler(logf)

    # Initialize CAN parser lib
    logger.info('Initialiazing...')
    can_msg = CanMsg()
    car_status = CarStatus()

    logger.info('Creating multicast socket.')
    mcast_sock = carlib.mcast_send_socket(addr=conf.MULTICAST_ADDR,
                                          port=conf.MULTICAST_PORT)
    logger.info('Opening serial port.')
    serial_dev = Serial(conf.SERIAL_DEV, conf.SERIAL_SPEED)

    logger.info('Starting ser2sock thread.')
    start_new_thread(ser2sock,
                     (serial_dev, mcast_sock, car_status, can_msg, logger,))

    logger.info('Startup procedure end.')
    while 42:
        sleep(3600)
        logger.info('-- mark --')

# EOF
