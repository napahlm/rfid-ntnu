import evdev
from evdev import categorize, ecodes

class Device():
    name = 'Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader'

    @classmethod
    def list(cls, show_all=False):
        # list the available devices
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if show_all:
            for device in devices:
                print("event: " + device.fn, "name: " + device.name, "hardware: " + device.phys)
        return devices

    @classmethod
    def connect(cls):
        # connect to device if available
        try:
            device = [dev for dev in cls.list() if cls.name in dev.name][0]
            device = evdev.InputDevice(device.fn)
            return device
        except IndexError:
            print("Device not found.\n - Check if it is properly connected. \n - Check permission of /dev/input/ (see README.md)")
            exit()

    @classmethod
    def reverseBytes(number):
        binary = "{0:0>32b}".format(number) # zero-padded 32-bit binary
        # split up in bytes and reverse them respectively
        byteList = [binary[i:i+8][::-1] for i in range(0, 32, 8)]
        return int(''.join(byteList), 2) # join list and convert binary to decimal

    @classmethod
    def run(cls):
        device = cls.connect()
        container = []
        try:
            device.grab()
            # bind the device to the script
            print("RFID scanner is ready....")
            print("Press Control + C to quit.")
            for event in device.read_loop():
                    # enter into an endeless read-loop
                    if event.type == ecodes.EV_KEY and event.value == 1:
                        digit = evdev.ecodes.KEY[event.code]
                        if digit == 'KEY_ENTER':
                            # create and dump the tag
                            tag = "".join(i.strip('KEY_') for i in container)
                            EM = reverseBytes(int(tag))
                            print("EM:" + EM)

                            container = []
                        else:
                            container.append(digit)

        except:
            # catch all exceptions to be able release the device
            device.ungrab()
            print('Quitting.')


Device.run()