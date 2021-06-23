#!/usr/bin/env python3
'''Trackpen - Emulate an Stylus with a touchpad'''
from evdev import InputDevice, list_devices, AbsInfo, ecodes
from evdev.uinput import UInput
from subprocess import Popen as sub

class Pen:
    def __init__(self, max_x_y):
        ''' Create an virtual pen and write data'''

        # Get max coordinates from touchpad
        pos_x       = max_x_y[0]
        pos_y       = max_x_y[1]

        # Pen model for UInput
        pointer_buttons = {
            ecodes.EV_KEY: [
                 ecodes.BTN_0,
                 ecodes.BTN_TOOL_PEN,
                 ecodes.BTN_TOOL_RUBBER,
                 ecodes.BTN_TOUCH,
                 ecodes.BTN_STYLUS,
                 ],
            ecodes.EV_ABS: [
                 (ecodes.ABS_X, pos_x),
                 (ecodes.ABS_Y, pos_y),
                 ]
            }
	# Pen device
        self.device = UInput(pointer_buttons, 'Virtual Pen', phys='virtual-pen' )

    def write(self, event_type, event_code, event_value):
        self.device.write(event_type, event_code, event_value)
        self.device.syn() # Force syncronization

class SystemTouchpad:
    def __init__(self):
        self.device = self.search_for_tps()

    def enable_tp_xinput(self):
        sub(['xinput',
             'enable',
             self.device.name])

    def disable_tp_xinput(self):
        sub(['xinput',
             'disable',
             self.device.name])

    def search_for_tps(self) -> InputDevice:
        ''' Return the first touchpad '''
        devices = [InputDevice(path) for path in list_devices()]
        touchpads = []

        for device in devices:
            capabilities = device.capabilities(absinfo=True)
            try:
                for key in capabilities[ecodes.EV_KEY]:
                    if key == ecodes.BTN_TOUCH:
                        touchpads.append(device)
            except KeyError:
                pass

        return touchpads[0]

    def get_abs_values(self) -> tuple:
        ''' Return device absolute info '''
        capabilities = self.device.capabilities(absinfo=True)
        x = capabilities[ecodes.EV_ABS][ecodes.ABS_X][1]
        y = capabilities[ecodes.EV_ABS][ecodes.ABS_Y][1]
        return (x, y)

    def loop(self, touchscreen):
        # Main loop
        rubber = 0
        pen = 1
        for event in self.device.read_loop():
            if event.type == ecodes.EV_ABS:
                touchscreen.write(event.type, event.code, event.value)
            elif event.type == ecodes.EV_KEY:
                if event.code == ecodes.BTN_LEFT:
                    touchscreen.write(event.type, ecodes.BTN_TOUCH, event.value)
                elif event.code == ecodes.BTN_TOOL_DOUBLETAP:
                    if event.value == 1:
                        if rubber == 0:
                            touchscreen.write(event.type, ecodes.BTN_TOOL_RUBBER, 1)
                            touchscreen.write(event.type, ecodes.BTN_TOOL_PEN, 0)
                            rubber = 1
                        else:
                            touchscreen.write(event.type, ecodes.BTN_TOOL_RUBBER, 0)
                            touchscreen.write(event.type, ecodes.BTN_TOOL_PEN, 1)
                            rubber = 0


if __name__ == '__main__':
    try:
        pad    = SystemTouchpad()
        screen = Pen(pad.get_abs_values())
        print("Disabling touchpad")
        pad.disable_tp_xinput()
        pad.loop(screen) 
    except KeyboardInterrupt:
        # Restore xinput touchpad on exit
        print('Restoring')
        pad.enable_tp_xinput()
