#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# BMW e87

from json import dumps

__name__ = 'carpcp_car'
__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'gerogi.kolev[at]gmail.com'


class CarStatus(object):
    def __init__(self):
        self.main = {}
        self.default()
        self.sched_list = [
            'throttle', 'coolant_temp', 'internal_temp', 'external_temp',
            'odmeter', 'key', 'engine', 'wheel_position', 'avr_fuel',
            'outside_temp', 'dip_beam', 'main_beam', 'full_beam',
            'reverse', 'handbrake', 'left_temp', 'right_temp']

    def get(self, arg):
        if arg in self.main:
            return self.main[arg]
        return False

    def set(self, var, val):
        if var in self.main:
            if val != self.main[var]:
                self.main[var] = val
                return dumps('%s=%s' % (var, val))
        else:
            self.main[var] = val
            return dumps('%s=%s' % (var, val))
        return False

    def default(self):
        """ Set default stuff """
        # Clock/Date
        self.main['seconds'] = 0
        self.main['minutes'] = 0
        self.main['hours'] = 0
        self.main['day'] = 1
        self.main['month'] = 1
        self.main['year'] = 2016
        # Key & Engine stuff
        self.main['rpm'] = 0
        self.main['key'] = False
        self.main['engine'] = 0
        self.main['throttle'] = 0
        self.main['torque'] = 0
        self.main['engine_status'] = 'Off'
        # Avrage stuff
        self.main['avr_fc'] = 0
        self.main['avr_fc100'] = 0
        self.main['avr_speed'] = 0
        # Misc stuff
        self.main['clutch'] = False
        self.main['brakes'] = False
        self.main['ragen'] = 0
        self.main['range1'] = 0
        self.main['reverse'] = False
        self.main['odmeter'] = 0
        self.main['avr_fuel'] = 0
        self.main['handbrake'] = False
        self.main['wheel_position'] = 0
        self.main['rear_demister'] = False
        # Wipers
        self.main['wipers'] = 0
        self.main['rear_wiper'] = 0
        self.main['wipers_speed'] = 0
        # Speed
        self.main['speed'] = 0
        self.main['rr_wheel'] = 0
        self.main['rl_wheel'] = 0
        self.main['fr_wheel'] = 0
        self.main['rl_wheel'] = 0
        # Car VIN/Last Reset/Production
        self.main['vin'] = False
        self.main['battery_reset'] = False
        self.main['production_date'] = False
        # Temperatures
        self.main['coolant_temp'] = 0
        self.main['outside_temp'] = 0
        self.main['internal_temp'] = 0
        self.main['external_temp'] = 0
        # Climate control
        self.main['fan_speed'] = 0
        self.main['left_temp'] = 0
        self.main['right_temp'] = 0
        # Lights
        self.main['hazard_lights'] = False
        self.main['left_turnsignal'] = False
        self.main['right_turnsignal'] = False
        self.main['dip_beam'] = False
        self.main['full_beam'] = False
        self.main['rear_fog'] = False
        self.main['front_fog'] = False
        self.main['main_beam'] = False
        self.main['brake_light'] = False
        self.main['cabinet_light'] = False
        # Wheel buttons (SZL)
        self.main['up_button'] = False
        self.main['down_button'] = False
        self.main['voice_button'] = False
        self.main['rotate_button'] = False
        self.main['telephone_button'] = False
        self.main['volumeup_button'] = False
        self.main['volumedown_button'] = False
        # Alarms
        self.main['door_alarm'] = False
        self.main['seatbelt_alarm'] = False
        # Doors/Hood/Boot
        self.main['hood'] = False
        self.main['boot'] = False
        self.main['rr_door'] = False
        self.main['rl_door'] = False
        self.main['fr_door'] = False
        self.main['fl_door'] = False
        # Locks
        self.main['boot_lock'] = False
        self.main['rr_lock'] = False
        self.main['rl_lock'] = False
        self.main['fr_lock'] = False
        self.main['fl_lock'] = False
        # Windows
        self.main['rr_window'] = 0
        self.main['rl_window'] = 0
        self.main['fr_window'] = 0
        self.main['fl_window'] = 0

    def add_second(self):
	if self.main['seconds'] < 59:
	    self.main['seconds'] += 1
	    if self.main['minutes'] < 59:
		self.main['minutes'] += 1
		if self.main['hours'] < 23:
		    self.main['hours'] += 1
		else:
		    self.main['hours'] = 0
	    else:
		self.main['minutes'] = 0
	else:
	    self.main['seconds'] += 0

    def scheduled(self):
        ret_list = []
        for el in self.sched_list:
            ret_list.append(
                dumps('%s=%s' % (el, self.get(el))))
        return ret_list

# EOF
