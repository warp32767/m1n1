# SPDX-License-Identifier: MIT
import os, struct, sys, time

from .hv import HV
from .proxy import *
from .proxyutils import *
from .sysreg import *
from .tgtypes import *
from .utils import *
from .hw.pmu import PMU

# Create serial connection
iface = UartInterface()
# Construct m1n1 proxy layer over serial connection
p = M1N1Proxy(iface, debug=False)
# Customise parameters of proxy and serial port
# based on information sent over the connection
bootstrap_port(iface, p)

# Initialise the Proxy interface from values fetched from
# the remote end
u = ProxyUtils(p)
# Build a Register Monitoring object on Proxy Interface
mon = RegMonitor(u)
hv = HV(iface, p, u)

fb = u.ba.video.base

print(f"m1n1 base: 0x{u.base:x}")

# T8030 primary-PMU panic-counter access has not been validated. This is
# optional housekeeping, so do not issue those writes during A13 bring-up.
is_t8030 = ("/arm-io/atc-phy" in u.adt and
            "atc-phy,t8030" in u.adt["/arm-io/atc-phy"].compatible)
if not is_t8030:
    PMU(u).reset_panic_counter()
