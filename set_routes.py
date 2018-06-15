#!/usr/local/bin/python
import netifaces
import netaddr
import subprocess
import os
from threading import Event
import pprint
import re


for iface in netifaces.interfaces():
    if iface.startswith("en"):
        for ifconf in  netifaces.ifaddresses(iface)[netifaces.AF_INET]:
            if ifconf['netmask'] != '255.255.255.255':
               break

# get current route destinations
routes = subprocess.check_output("route")
destinations = []

for line in routes.split("\n"):
    if re.match("^\d+\.\d+\.\d+\.\d+.*", line):
        destinations.append(line.split()[0])

network = netaddr.IPNetwork("%s/%s" % (ifconf['addr'], ifconf['netmask']))


gws = netifaces.gateways()
default_gw = gws['default'][netifaces.AF_INET]

for ip in network:
    if ip != network.network and ip != network.broadcast and ip != netaddr.IPAddress(default_gw[0]) and str(ip) not in destinations:
        subprocess.call(["route", "add", "-host", str(ip),  "gw", default_gw[0]])

Event.wait()
