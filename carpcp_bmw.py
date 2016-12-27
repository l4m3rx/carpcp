#!/usr/bin/env python
#
# BMW e87 CAN Lib-ish thingy
#
# ## What's working ###
#  - RPM
#  - Speed
#  - Throttle Position
#  - Coolant Temperature
#  - Steering Wheel Position
#
#  - Key Status
#  - Engine Status
#
#  - Reverse Gear / Light
#  - Handbrake Status
#
#  - Brake Light
#  - Dip/Main/Full Beams
#  - Front/Rear Fog Lights
#  - Turn signals/ Hazard lights
#
#  - Odometer
#  - Average Speed
#  - Average Fuel Level
#  - Average Fuel Consumation
#  - Range (Expected range with current fuel/consumation)
#
#  - SZL buttons
#  - Window position
#  - Open Door Alarm
#  - Door Open/Close Lock/Unlock Status
#
#  - Rear Wiper Status
#  - Front Wipers Speed / Status
#
#  - Outside Temp
#  - Rear Demister Status
#  - Internal Temp / Internal Light
#  - Aircondition Left/Right Temperature Setting
#
#  - Individual Wheel Speed
#
#  - Production Date
#  - Last Battery Reset
#
# ##  Broken data  ###
#  - Voltage
#  - Torque, KW, HP
#  - Dashboard dimmer
#
# ##  TODO  ###
#  - Air condition status
#    * Air direction(s)
#    * REST Function On/Off
#  - VIN (Packets is sent pretty rearly :( )
#


import carpcp_car as car

__name__ = 'carpcp_car'
__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'georgi.kolev[at]gmail.com'


class CarStatus(object):
    def __init__(self):
        self.car = car.CarStatus()

    def get(self, arg):
        return self.car.get(arg)

    def set(self, var, val):
        return self.car.set(var, val)

    def decode_vin(self, msg):
        try:
            self.set('vin', map(chr, msg[::-1]))
        except:
            return False

    def get_time(self):
        return '%s:%s:%s' % (self.car.get('hours'),
                             self.car.get('minutes'),
                             self.car.get('seconds'))

    def get_datee(self):
        return '%s:%s:%s' % (self.car.get('day'),
                             self.car.get('month'),
                             self.car.get('year'))

    def add_second(self):
        # We sync the clock every 30s, so even
        # if we go to hours=25 it will be fixed fast
        # Its just a waste of time to go futher
        self.car.add_second()

    def msg(self, m):
        result = []
        # Message sanity checks
        if not (hasattr(m, 'mid') and hasattr(m, 'mlen')):
            return False
        if m.mlen < 1:
            return False

        if (m.mid == 0x130) and (m.mlen > 1):
            if m.message[0] == 0:
                result.append(self.set('engine', 0))
                result.append(self.set('engine_status', 'Off'))
            elif m.message[0] == 0x40:
                result.append(self.set('engine', 0))
                result.append(self.set('engine_status', 'Off'))
            elif m.message[0] == 0x41:
                result.append(self.set('engine', 1))
                result.append(self.set('engine_status', 'Ready'))
            elif m.message[0] == 0x45:
                result.append(self.set('engine', 2))
                result.append(self.set('engine_status', 'Running'))
            if m.message[1] == 0x40:
                result.append(self.set('key', 1))
                result.append(self.set('key_status', 'True'))
            elif m.message[1] == 0:
                result.append(self.set('key', 0))
                result.append(self.set('key_status', 'False'))
                # ... http://www.loopybunny.co.uk/CarPC/can/130.html
        elif (m.mid == 0x1B4) and (m.mlen > 1):
            self.mph = (((m.message[1] - 0xC0) * 256) + m.message[0]) / 16
            self.kph = (self.mph * 1.61)
            result.append(self.set('speed', self.kph))
            if m.message[5] == 50:
                result.append(self.set('handbrake', 1))
            elif m.message[5] == 48:
                result.append(self.set('handbrake', 0))
        elif (m.mid == 0x1D0):
            result.append(self.set('coolant_temp', (m.message[0] - 48)))
        elif (m.mid == 0x1D6) and (m.mlen > 1):
            if (m.message[0] == 0xC0) and (m.mlen > 1):
                if m.message[1] == 0xD:
                    print('[%s] Voice button' % self.get_time())
                    result.append('voice_button=1')
                    result.append('next_track=1')
                    # client.next()
                elif m.message[1] == 0x1C:
                    result.append('rotate=1')
                    print('[%s] Rotate button' % self.get_time())
                elif m.message[1] == 0x4C:
                    result.append('disk_button=1')
                    print('[%s] Change disk button' % self.get_time())
            elif (m.message[0] == 0xC1) and (m.message[1] == 0xC):
                result.append('telephone_button=1')
                result.append('prev_track=1')
                # client.previous()
                print('[%s] Telephone button' % self.get_time())
            elif (m.message[0] == 0xC4) and (m.message[1] == 0xC):
                result.append('volumedown_button=1')
                print('[%s] Volume down' % self.get_time())
            elif (m.message[0] == 0xC8) and (m.message[1] == 0xC):
                result.append('volumeup_button=1')
                print('[%s] Volume up' % self.get_time())
            elif (m.message[0] == 0xD0) and (m.message[1] == 0xC):
                result.append('down_button=1')
                print('[%s] Down button' % self.get_time())
            elif (m.message[0] == 0xE0) and (m.message[1] == 0xC):
                result.append('up_button=1')
                print('[%s] Up button' % self.get_time())
        elif (m.mid == 0x1F6) and (m.mlen > 1):
            if m.message[0] == 0x80:
                result.append(self.set('hazard_lights', 0))
                result.append(self.set('left_turnsignal', 0))
                result.append(self.set('right_turnsignal', 0))
            elif (m.message[0] == 0x91):
                result.append(self.set('left_turnsignal', 1))
            elif (m.message[0] == 0xA1):
                result.append(self.set('right_turnsignal', 1))
            elif (m.message[0] == 0xB1):
                result.append(self.set('hazard_lights', 1))
        elif (m.mid == 0x1EE):
            if m.message[0] == 0x00:
                result.append(self.set('full_beam', 0))
                result.append(self.set('left_turnsignal', 0))
                result.append(self.set('right_turnsignal', 0))
            elif m.message[0] == 0x02:
                result.append(self.set('left_turnsignal', 0))
                result.append(self.set('right_turnsignal', 1))
            elif m.message[0] == 0x08:
                result.append(self.set('left_turnsignal', 1))
                result.append(self.set('right_turnsignal', 0))
            elif m.message[0] == 0x10:
                result.append(self.set('full_beam', 1))
            elif m.message[0] == 0x01:
                print('[%s] Right turnsignal (blink)' % self.get_time())
            elif m.message[0] == 0x04:
                print('[%s] Left turnsignal (blink)' % self.get_time())
            elif m.message[0] == 0x20:
                print('[%s] Flash High Beam' % self.get_time())
        elif (m.mid == 0x24B):
            if m.message[0]:
                result.append(self.set('door_alarm', 1))
            else:
                result.append(self.set('door_alarm', 0))
        elif (m.mid == 0x202):
            # http://www.loopybunny.co.uk/CarPC/can/202.html
            self.dashboard_dimmer = int((255 - m.message[0]) / 25)
        elif (m.mid == 0x21A) and (m.mlen > 1):
            # http://www.loopybunny.co.uk/CarPC/can/21A.html
            bmsg1 = biny(m.message[0], 8)
            bmsg2 = biny(m.message[1], 8)
            result.append(self.set('rear_fog', bmsg1[1]))
            result.append(self.set('dip_beam', bmsg1[5]))
            result.append(self.set('main_beam', bmsg1[7]))
            result.append(self.set('front_fog', bmsg1[2]))
            result.append(self.set('brake_light', bmsg1[0]))
            result.append(self.set('interior_light', bmsg2[6]))
        elif (m.mid == 0x1E3) and (m.mlen > 1):
            if m.message[0] == 0xF1:
                result.append(self.set('cabinet_light', 1))
            else:
                result.append(self.set('cabinet_light', 0))
        elif (m.mid == 0x328) and (m.mlen > 5):
            pd = '0x%s%s%s%s' % (m.message[3], m.message[2],
                                 m.message[1], m.message[0])
            br = '0x%s%s' % (m.message[5], m.message[4])
            # Battery reset is in days since 01/01/2000
            # Production date is seconds since the production date
            result.append(self.set('battery_reset', int(br, 16)))
            result.append(self.set('production_date', (int(pd, 16)/(60*24))))
        elif (m.mid == 0x246) and m.mlen:
            if m.message[0] == 0x3F:
                result.append(self.set('rear_demister', 0))
            elif m.message[0] == 0x7F:
                result.append(self.set('rear_demister', 1))
        elif (m.mid == 0x26E):
            if (m.message[0] == 0) and \
                    (m.message[1] == 0x40) and (m.message[2] == 0x7F):
                result.append(self.set('1key', 1))
                result.append(self.set('1key_status', 'True'))
            elif ((m.message[0] and m.message[1]) == 0) \
                    and (m.message[2] == 0x3F):
                result.append(self.set('1key', 1))
                result.append(self.set('1key_status', 'True'))
            elif ((m.message[0] and m.message[1]) == 0x40) \
                    and (m.message[2] == 0x7F):
                result.append(self.set('key', 1))
                result.append(self.set('1key_status', 'True'))
        elif (m.mid == 0x2A6):
            if m.message[0] == 0x00:
                result.append(self.set('wipers', 0))
                result.append(self.set('rear_wiper', 0))
            elif (m.message[0] == 0x01) and (m.mlen > 1):
                result.append(self.set('wipers', 1))
                result.append(self.set('wipers_speed', (m.message[1] - 247)))
            elif (m.message[0] in [0x40, 0x81, 0x10]) and (m.mlen > 1):
                result.append(self.set('rear_wiper', 1))
            elif (m.message[0] == 0x08) and (m.mlen > 1):
                print('[%s] Single wipe' % (self.get_time()))
        elif (m.mid == 0x2CA):
            result.append(self.set('outside_temp', ((m.message[0] - 80) / 2)))
        elif (m.mid == 0x2E6) and (m.mlen == 8):
            result.append(self.set('left_temp', (m.message[7] / 2.0)))
            result.append(self.set('fan_speed', (m.message[5])))
        elif (m.mid == 0x2EA) and (m.mlen == 8):
            result.append(self.set('right_temp', (m.message[7] / 2.0)))
        elif (m.mid == 0x366) and (m.mlen > 2):
            etemp = (m.message[0] - 80) / 2.0
            erange = '0x%s%s' % (hex(m.message[2])[2:], hex(m.message[1])[2:])
            result.append(self.set('external_temp', etemp))
            result.append(self.set('range1', int(erange, 16)/16))
        elif (m.mid == 0x330) and (m.mlen == 8):
            odm = '0x%s%s%s' % (hex(m.message[2])[2:].upper().rjust(2),
                                hex(m.message[1])[2:].upper().rjust(2),
                                hex(m.message[0])[2:].upper().rjust(2))
            odm = odm.replace(' ', '0')
            range0 = '0x%s%s' % (hex(m.message[7])[2:].upper().rjust(2),
                                 hex(m.message[6])[2:].upper().rjust(2))
            range0 = range0.replace(' ', '0')
            result.append(self.set('odometer', int(odm, 16)))
            result.append(self.set('avr_fuel', m.message[3]))
            result.append(self.set('range', int(range0, 16) / 16))
        elif (m.mid == 0x34F):
            if m.message[0] == 0xFE:
                result.append(self.set('handbrake', 1))
            elif m.message[0] == 0xFD:
                result.append(self.set('handbrake', 0))
        elif (m.mid == 0x2FC) and (m.mlen > 2):
            # Doors
            bmsg = biny(m.message[1], 8)
            bmsg2 = biny(m.message[2], 8)
            result.append(self.set('rr_door', bmsg[1]))
            result.append(self.set('rl_door', bmsg[3]))
            result.append(self.set('fr_door', bmsg[5]))
            result.append(self.set('fl_door', bmsg[7]))
            # Bonnet & Boot
            # It appears e87 dosnt have hood status here
            # It is probably populated by another message.
            # result.append(self.set('bonnet_open', bmsg2[1]))
            result.append(self.set('boot_open', bmsg2[7]))
#        elif (m.mid == 0x2D6) and (m.mlen > 1):
#         # Looks like e87 donst use this for message for
#         # the aircondition status...probably another message?
#             print '2D6', m.message
#            if m.message[1] == 0xFC:
#                result.append(self.set('aircondition', 0))
#            elif m.message[1] == 0xFD:
#                result.append(self.set('aircondition', 1))
        elif (m.mid == 0x32E) and (m.mlen > 3):
            self.internal_light = m.message[0]
            result.append(
                self.set('internal_temp', ((m.message[3] / 10.0) + 6))
            )
        elif (m.mid == 0x349) and (m.mlen > 3):
            self.left_fuel = binc(m.message[0], m.message[1]) / 160
            self.right_fuel = binc(m.message[2], m.message[3]) / 160
#            print self.left_fuel, 'fuel left', self.right_fuel
        elif (m.mid == 0x362) and (m.mlen > 2):
            # Constant: 235.214
            hb, lb = hl_bits(m.message[1])
            afc = binc(m.message[2], hb)
            akmph = binc(m.message[0], lb)
            # Fuel consumation error!!! close but ...
            result.append(self.set('avr_fc', afc / 10.0))
            result.append(self.set('avr_speed', akmph / 10.0))
            result.append(
                self.set('avr_fc100', round((235.214 / self.avr_fc), 2)))
        elif (m.mid == 0x380) and (m.mlen == 7):
            self.decode_vin(m.message)
        elif m.mid == 0xF2:
            if m.message[0] == 241:
                result.append(self.set('boot_locked', 0))
            elif m.message[0] > 241:
                result.append(self.set('boot_locked', 1))
#            if m.message[3] == 192:
#                result.append(self.set('boot_open', 0))
#            elif m.message[3] == 193:
#                result.append(self.set('boot_open', 1))
        elif m.mid == 0xEE:
            if m.message[0] == 0x81:
                result.append(self.set('rl_lock', 0))
            elif m.message[0] > 0x81:
                result.append(self.set('rl_lock', 1))
#            if m.message[3] == 0xFC:
#                result.append(self.set('rl_door', 1))
#            elif m.message[3] == 0xFD:
#                result.append(self.set('rl_door', 0))
        elif m.mid == 0xEA:
            if m.message[0] == 0x81:
                result.append(self.set('rr_lock', 0))
            elif m.message[0] > 0x81:
                result.append(self.set('rr_lock', 1))
        elif m.mid == 0xE6:
            if m.message[0] == 0x81:
                result.append(self.set('fr_lock', 0))
            elif m.message[0] > 0x81:
                result.append(self.set('fr_lock', 1))
        elif m.mid == 0xE2:
            if m.message[0] == 0x81:
                result.append(self.set('fl_lock', 0))
            elif m.message[0] > 0x81:
                result.append(self.set('fl_lock', 1))
        elif (m.mid == 0x3B0):
            if m.message[0] == 0xFD:
                result.append(self.set('reverse', 0))
            elif m.message[0] == 0xFE:
                result.append(self.set('reverse', 1))
        elif (m.mid == 0x3B6):
            result.append(self.set('fl_window', m.message[0]))
        elif (m.mid == 0x3B7):
            result.append(self.set('rl_window', m.message[0]))
        elif (m.mid == 0x3B8):
            result.append(self.set('fr_window', m.message[0]))
        elif (m.mid == 0x3B9):
            result.append(self.set('rr_window', m.message[0]))
        elif (m.mid == 0x2F8) and (m.mlen > 6):
            hb, lb = hl_bits(m.message[4])
            month = '0x%s' % hb
            month = int(month, 16)
            result.append(self.set('month', month))
            result.append(self.set('day', m.message[3]))
            result.append(self.set('hours', m.message[0]))
            result.append(self.set('minutes', m.message[1]))
            result.append(self.set('seconds', m.message[2]))
            result.append(self.set('year', binc(m.message[5], m.message[6])))
        elif (m.mid == 0x2B6):
            # Not yet sure what this message is
            # But its transmitted every 1 seconds, so i'll use it
            # to keep track the clock in check.
            self.add_second()
        elif (m.mid == 0x3B4) and (m.mlen > 1):
            # Gives values of 60 all the the time... probably we need another ID
            cv = (((m.message[1] - 240) * 256) + m.message[0]) / 68
            result.append(self.set('voltage', cv))
        elif (m.mid == 0x581) and (m.mlen > 3):
            if m.message[3] == 0x28:
                result.append(self.set('seat_belt_alarm', 0))
        elif (m.mid == 0x394) and (m.mlen > 3):
            if m.message[3] == 0x29:
                result.append(self.set('seat_belt_alarm', 1))
        elif (m.mid == 0xA8) and (m.mlen == 8):
            result.append(self.set('brake_power', m.message[7]))
            # torque = ((m.message[2] * 256) + m.message[1]) / 32
#            result.append(self.set('torque', torque/100.0)
#            self.calc_kw()
            if m.message[5] == 0xF0:
                result.append(self.set('clutch', 0))
            elif m.message[5] == 0xF1:
                result.append(self.set('clutch', 1))
            if m.message[7] > 20:
                result.append(self.set('brakes', 1))
            else:
                result.append(self.set('brakes', 0))
        elif (m.mid == 0xAA) and (m.mlen > 6):
            rpm = binc(m.message[4], m.message[5]) / 4
            throttle = binc(m.message[2], m.message[3]) / 256
            result.append(self.set('rpm', rpm))
            result.append(self.set('throttle', throttle))
        elif (m.mid == 0xC8) and (m.mlen > 1):
            bm = binc(m.message[0], m.message[1])
            if (bm / 23) > 360:
                wheel_position = (bm - 65535) / 23
            else:
                wheel_position = bm/23
            if (wheel_position < 360) and (wheel_position > -360):
                result.append(self.set('wheel_position', wheel_position))
        elif (m.mid == 0xCE) and (m.mlen == 8):
            # 1.6 to get in km/h not mph
            self.set('fl_wheel', (binc(m.message[0], m.message[1]) / 24 * 1.6))
            self.set('fr_wheel', (binc(m.message[3], m.message[3]) / 24 * 1.6))
            self.set('rl_wheel', (binc(m.message[4], m.message[5]) / 24 * 1.6))
            self.set('rr_wheel', (binc(m.message[6], m.message[7]) / 24 * 1.6))
        elif (m.mid == 0x2A0):
            # http://www.e90post.com/forums/showpost.php?p=14513521&postcount=114
            # ID:2A0 [8] DATA:88 88 80 0 16 40 86 0
            # I've been able to open the trunk.
            # Hope this is helpful for somebody.
            #
            # ID: 2a0 -0- Data: [8]  88 88 88 1 2c 40 6 0
            # This should be normal status?
            pass
        elif (m.mid == 0x2F0):
            pass  # ID: 2f0 -0- Data: [2]  f7 fc
        elif (m.mid == 0x23A):
            print 'ID: 0x23A', m.message
        elif (m.mid == 0x2F4):
            pass  # ID: 2f4 -0- Data: [4]  cf ff ff ff
        elif (m.mid == 0x2F6):
            pass  # ID: 2f6 -0- Data: [2]  0 f5
        elif (m.mid == 0x2FA):
            pass  # ID: 2fa -0- Data: [5]  fd 8 ff ff ff
        elif (m.mid == 0x311):
            pass  # ID: 311 -0- Data: [2]  0 f0
        elif (m.mid == 0x335):
            pass  # Sensor data?! Inspect more
        elif (m.mid == 0x367):
            pass  # Sensor data?! Inspect more
        elif (m.mid == 0x35C):
            pass  # ID: 35c -0- Data: [4]  ff f0 ff a0
        elif (m.mid == 0x3B3):
            pass  # ID: 3b3 -0- Data: [6]  11 c8 0 0 0 f0
        elif (m.mid == 0x3BD):
            pass  # ID: 3bd -0- Data: [2]  fd ff
        elif (m.mid == 0x3BE):
            pass  # ID: 3be -0- Data: [2]  fe ff
        elif (m.mid == 0x360):
            pass  # ID: 360 -0- Data: [7]  ff ff ff ff ff ff ff
        elif (m.mid == 0x364):
            pass  # ID: 364 -0- Data: [7]  ff ff ff ff ff ff ff
        elif (m.mid == 0x35E):
            pass  # ID: 35e -0- Data: [8]  ff ff ff ff ff ff ff ff
        elif (m.mid == 0xD7):
            pass  # Seat belt & airbag relayted counter
        elif (m.mid == 0xC0):
            pass  # ABS / Brake counter
        elif (m.mid == 0xC4):
            pass  # Same as 0xC8 (not sent as often thou)
        elif (m.mid == 0x2BA):
            pass  # Counter (Toggle / Heartbeat)
        elif (m.mid == 0x19E):
            # Get brake pressure?
            pass  # ABS Stuff http://www.loopybunny.co.uk/CarPC/can/19E.html
        elif (m.mid == 0x7C3):
            pass    # Keyfob (security,comfort and CBS data). # To inspect more
        elif (m.mid == 0x1A6):
            pass     # Speed used by instrument cluster (offsets)
        elif (m.mid == 0x1A0):
            pass

        else:
            # print hex(m.mid), ' '.join(map(hex, m.message))
            idstr = str(hex(m.mid))
            if idstr in self.uids:
                self.uids[idstr] += 1
            else:
                self.uids[idstr] = 1
        res = []
        for el in result:
            if el:
                res.append(el)

        return res

    def unknown_ids(self):
        return self.uids

    def calc_kw(self):
        # (RPM * Torque) / ()60 / 2Pi) / 1000
        self.kw = ((self.rpm * self.torque) * 9.54) / 1000


def binc(i, n):
    return (n * 256) + i


def biny(i, l):
    return format(i, 'b').zfill(l)


def hl_bits(i):
    bb = hex(i)[2:]
    return int(bb[0], 16), int(bb[1], 16)

# EOF