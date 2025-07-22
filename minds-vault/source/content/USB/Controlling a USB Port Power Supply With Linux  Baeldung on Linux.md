---
{"publish":true,"title":"Controlling a USB Port Power Supply With Linux | Baeldung on Linux","description":"Learn several ways of controlling the power supply to a USB port in Linux.","created":"2025-02-06T12:46:26.796+01:00","modified":"2025-07-07T12:01:13.300+02:00","tags":["clippings"],"cssclasses":""}
---

## 1. Introduction

If we’re working on a Linux system and need to toggle a [USB port power supply](https://www.baeldung.com/linux/usb-port-power), there are a few ways to do it.

In this tutorial, we’ll explore how to control the power supply of a USB port using Linux.

Notably, **certain USB devices may have built-in protections or firmware settings that prevent unauthorized changes to their power settings for safety or operational reasons**.

## 2\. Using */sys/bus/usb*By writing specific values to the [*/sys*](https://www.baeldung.com/linux/find-device-driver#the-sysfs-pseudo-filesystem) pseudo-filesystem *power/control* file for a USB device, we can influence its power-related behavior. For example, we can turn on or off the USB port and toggle the [*autosuspend*](https://www.kernel.org/doc/Documentation/usb/power-management.txt) functionality.

Thus, we’ll use [*echo*](https://www.baeldung.com/linux/echo-command) in combination with file [redirection](https://www.baeldung.com/linux/pipes-redirection) to write a value to the respective control file of a USB device.

First, let’s find the device’s USB port using [*dmesg*](https://www.baeldung.com/linux/dmesg-convert-timestamp#the-dmesg-command) and [*grep*](https://www.baeldung.com/linux/common-text-search):

```bash
$ dmesg | grep "usb"
dmesg | grep "usb"
[    0.325546] usbcore: registered new interface driver usbfs
[    0.325589] usbcore: registered new interface driver hub
[    0.325616] usbcore: registered new device driver usb
[    0.487210] pci 0000:00:1d.0: quirk_usb_early_handoff+0x0/0x140 took 33353 usecs
[    0.680250] usb usb1: New USB device found, idVendor=1d6b, idProduct=0002, bcdDevice= 5.14
[    0.680263] usb usb1: New USB device strings: Mfr=3, Product=2, SerialNumber=1
[    0.680276] usb usb1: Product: EHCI Host Controller
[    0.680288] usb usb1: Manufacturer: Linux 5.14.0-299.el9.x86_64 ehci_hcd
...
[38484.380733] usb 1-3: USB disconnect, device number 10
[38614.274597] usb 1-3: new high-speed USB device number 11 using ehci-pci
[38614.406083] usb 1-3: New USB device found, idVendor=090c, idProduct=1000, bcdDevice=11.00
[38614.406097] usb 1-3: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[38614.406099] usb 1-3: Product: USB Flash Disk
[38614.406100] usb 1-3: Manufacturer: P-net
[38614.406101] usb 1-3: SerialNumber: 0360915110000723
[38614.411735] usb 1-3:1.0: USB P-net Fan device detected
```

In this example, we searched for lines in the kernel message log that contain the keyword *usb*. From the output, we got data about our USB port devices such as *Manufacturer*, *SerialNumber*, *idVendor*, and *idProduct*. In this case, *1-3:1.0* indicates that the USB fan device is connected to *bus 1*, *port 3*, and has a configuration or interface of *1.0*.

Now, we can disable *autosuspend* of our USB device:

```bash
$ echo "0" > "/sys/bus/usb/devices/1-3:1.0/power/autosuspend_delay_ms"
```

To be clear, ***autosuspend* is a feature that allows the system to automatically suspend power to idle USB devices to save energy**. By setting *autosuspend* to *0*, we disable this behavior for our device. Importantly, *1-3:1.0* is the exact number we got from the previous step.

Then, we can turn off our USB device:

```bash
$ echo "auto" > "/sys/bus/usb/devices/1-3:1.0/power/control"
```

Here, *auto* indicates that the power management should be handled automatically by the system or [device driver](https://www.baeldung.com/linux/find-device-driver). **The system determines when to suspend or resume power for the USB device based on its activity or idle state**.

Finally, we can check the status of our USB device by reading back the respective *runtime\_status* file via [*cat*](https://www.baeldung.com/linux/files-cat-more-less#cat):

```bash
$ cat /sys/bus/usb/devices/1-3:1.0/power/runtime_status
suspended
```

As we can see, our USB device is suspended.

Now, we can turn our device on again:

```bash
$ echo "on" > "/sys/bus/usb/devices/1-3:1.0/power/control"
```

Finally, let’s recheck the status:

```bash
$ cat /sys/bus/usb/devices/1-3:1.0/power/runtime_status
active
```

Here, we can see the USB device is active again.

## 3\. Using *uhubctl*[*uhubctl*](https://manpages.ubuntu.com/manpages/focal/man8/uhubctl.8.html) is a command-line utility that allows us to control the USB power of individual ports on smart USB hubs. ***uhubctl* doesn’t directly control power to other types of USB devices such as flash drives or keyboards**.

First, we install the *uhubctl* command via [*apt-get*](https://www.baeldung.com/linux/yum-and-apt#2-apt-get):

```bash
$ sudo apt-get install uhubctl
```

Then, we run the *uhubctl* command to list available hubs and ports:

```bash
$ sudo uhubctl
Current status for hub 1-1 [046d:0821 Logitech Smart USB Hub, USB 2.0, 7 ports]
  Port 1: 0100 power fan
  Port 2: 0100 power
  Port 3: 0100 power
  Port 4: 0100 power
  Port 5: 0100 power
  Port 6: 0100 power
  Port 7: 0100 power
```

In this example, we can see all our smart USB hub ports are powered on and that **a fan is connected to *port 1***.

So, let’s turn off the fan’s port:

```bash
$ sudo uhubctl -a off -p 1
Current status for hub 1-1 [046d:0821 Logitech Smart USB Hub, USB 2.0, 7 ports]
 Port 1: 0100 power
Sent power off request
New status for hub 1-1 [046d:0821 Logitech Smart USB Hub, USB 2.0, 7 ports]
 Port 1: 0000 off
```

Notably, we used *\-a off* to specify that our action is off. Moreover, *\-p* determines the port. In this case, **a power *off* request was sent to *port 1*, and the status changed to *0000* which means our port’s power supply is now off**.

At this point, we can turn the port back on:

```bash
$ sudo uhubctl -a on -p 1
Current status for hub 1-1 [046d:0821 Logitech Smart USB Hub, USB 2.0, 7 ports]
 Port 1: 0000 off
Sent power off request
New status for hub 1-1 [046d:0821 Logitech Smart USB Hub, USB 2.0, 7 ports]
 Port 1: 0100 power
```

In this case, a power *on* request was sent to *port 1*, and the current status of our port is back to *0100*, meaning power is *on*.

## 4. Using Udev Rules

[*udev*](https://www.baeldung.com/linux/monitor-device-events#basics-of-device-events-in-linux) is a Linux utility that manages device events. Moreover, [*udev* rules](https://www.baeldung.com/linux/automount-usb-device#1-creating-an-udev-rule) are custom configurations that define actions for specific devices based on their attributes. **With *udev* rules, we can control USB power and perform various automated actions directly from the command line in Linux**.

There are several ways to get information about connected USB devices such as *dmesg*, [*lsusb*](https://www.baeldung.com/linux/check-for-usb-devices#usinglsusb), and [inspecting */usb/devices*](https://www.baeldung.com/linux/check-for-usb-devices#usinglsusb).

First, let’s get information about our USB device:

```bash
$ sudo lsusb
Bus 001 Device 014: ID 203a:fffc PARALLELS Virtual Mouse
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 010: ID 12d1:140c Huawei Technologies Co., Ltd. E180v
Bus 002 Device 009: ID 203a:fffe PARALLELS Virtual USB1.1 HUB
Bus 002 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
```

Here, we can see the list of our USB devices. Moreover, the string after *ID* is the *idVendor* and *idProduct*. In this case, **we have *12d1:140c* for the device of interest: *Huawei Technologies Co., Ltd. E180v***.

Then, we can create a *udev* rule file using any text editor, such as [*nano*](https://www.baeldung.com/linux/files-vi-nano-emacs#nano):

```bash
$ nano /etc/udev/rules.d/usb-power.rules
```

Now, we can add this rule:

```bash
ACTION=="add", SUBSYSTEM=="usb", ATTR{idVendor}=="12d1", ATTR{idProduct}=="140c", ATTR{power/control}="auto"
```

Let’s break down this rule:

- *ACTION==”add”* – defines the action that triggers the rule
- *SUBSYSTEM==”usb”* – matches the subsystem of the device
- *ATTR{idVendor}==”12d1″* – *idVendor* of the USB device
- *ATTR{idProduct}==”140c”* – *idProduct* of the USB device
- *ATTR{power/control}=”auto”* – sets the value of the power or control attribute to *auto*

Then, we need to reload the *udev* rules for the changes to take effect:

```bash
$ sudo udevadm control --reload-rules
```

In this case, we used [*udevadm*](https://www.baeldung.com/linux/monitor-device-events#monitor-device-events-with-udevadm), a command-line tool for managing and querying the *udev* device manager. Moreover, we used *control –reload-rules* to ask the *udev* daemon to reload the *udev* rules.

## 5\. Using *hub-ctrl*[*hub-ctrl*](https://github.com/yy502/hub-ctrl) is a Linux command-line utility that controls the power supply of USB hub ports, enabling users to programmatically turn USB devices on or off. Moreover, ***hub-ctrl* simplifies USB power management, allowing for automation and customization according to user preferences**.

### 5.1. Installation

First, we need to install dependencies:

```bash
$ sudo apt-get install libusb-dev gcc
```

Then, we can get *hub-ctl* via [*git*](https://www.baeldung.com/git-guide):

```bash
$ git clone https://github.com/yy502/hub-ctrl
```

Now, we’ll navigate to the *hub-ctrl* directory:

```bash
$ cd hub-ctrl
```

Then, we’ll compile *hub-ctrl* using [*gcc*](https://www.baeldung.com/cs/how-compilers-work):

```bash
$ gcc -o hub-ctrl hub-ctrl.c -lusb -std=c99
```

Here, we compiled the *hub-ctrl.c* source code file and generated an executable binary file named *hub-ctrl*. Moreover, we used the *\-lusb* option to use [*libusb*](https://libusb.info/) library during the compilation process. Afterward, we used *\-std=c99* to set the C language standard to C99.

### 5.2. Control USB Power

Now, we can list hubs and ports directly with *hub-ctrl* instead of using another tool:

```bash
$ sudo ./hub-ctrl 
Hub 0 (Bus 4, Dev 1) - ganged power switching
Hub 1 (Bus 3, Dev 1) - no power switching
 ├─ Port  1: power
 └─ Port  2: power
Hub 2 (Bus 2, Dev 1) - no power switching
 ├─ Port  1: power
 └─ Port  2: power
Hub 3 (Bus 1, Dev 1) - no power switching
 ├─ Port  1: power high-speed connect enable
...
 ├─ Port 14: power
 └─ Port 15: power
```

The output is a comprehensive tree view of the requested devices.

Finally, we can turn off the port of interest:

```bash
$ sudo ./hub-ctrl -H 3 -P 1 -p 0
> Hub:3 Bus:0 Devive:0 Port:1 power->off
```

Here, we use several options:

- *\-H* – hub number
- *\-P* – port number
- *\-p 0* – turn off the power

Moreover, we can use bus, device, and port numbers:

```bash
$ sudo ./hub-ctrl -B 1 -D 1 -P 1 -p 0
> Hub:3 Bus:1 Devive:1 Port:1 power->off
```

Here, we used *\-B* to define the bus number and *\-D* to set the device number.

Conversely, we can turn the power back on for the same USB port:

```bash
$ sudo ./hub-ctrl -B 1 -D 1 -P 1 -p 1
> Hub:3 Bus:1 Devive:1 Port:1 power->on
```

As we can see, the *\-p 1* option means turning on the power.

## 6. Conclusion

In this article, we looked at several methods for controlling USB port power supply on Linux systems. Firstly, we used the *echo* command to manipulate the *power/control* file of the USB device. In particular, we disabled *autosuspend*, and controlled the power state. Secondly, we used the *uhubctl* command to control USB port power on smart USB hubs individually.

Afterward, the third technique involved creating custom *udev* rules to automate actions based on specific USB device attributes. Lastly, we explored the *hub-ctrl* utility, which allowed for controlling power to individual ports on a USB hub.

To sum up, these methods offer flexibility and control over USB port power management, enabling us to customize our system’s behavior according to our specific requirements.