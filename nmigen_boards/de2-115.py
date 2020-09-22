import os
import subprocess

from nmigen.build import *
from nmigen.vendor.intel import *

from .resources import *

__all__ = ["DE2115Platform"]


class DE2115Platform(IntelPlatform):
    device = "EP4CE115"  # Cyclone IV
    package = "F29"
    speed = "C8"
    default_clk = "clk50"
    resources = [
        Resource("clk50", 0, Pins("Y2", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 1, Pins("AG14", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),
        Resource("clk50", 2, Pins("AG15", dir="i"),
                 Clock(50e6), Attrs(io_standard="3.3-V LVTTL")),

        *LEDResources(0,
                      pins="E21 E22 E25 E24 H21 G20 G22 G21",
                      attrs=Attrs(io_standard="2.5 V")),
        *LEDResources(1,
                      pins="E21 E22 E25 E24 H21 G20 G22 G21",
                      attrs=Attrs(io_standard="2.5 V")),
        *ButtonResources(
            pins="M23 M21 N21 R24",
            attrs=Attrs(io_standard="2.5 V")),
        *SwitchResources(
            pins="AB28 AC28 AC27 AD27 AB27 AC26 AD26 AB26 AC25 AB25 AC24 AB24 AB23 AA24 AA23 AA22 Y24 Y23",
            attrs=Attrs(io_standard="2.5 V")),

        UARTResource(0,
                     rx="G12", tx="G9", rts="J13", cts="G14",
                     attrs=Attrs(io_standard="3.3-V LVTTL")),
    ]
    connectors = []

    def toolchain_program(self, products, name):
        quartus_pgm = os.environ.get("QUARTUS_PGM", "quartus_pgm")
        with products.extract("{}.sof".format(name)) as bitstream_filename:
            subprocess.check_call([quartus_pgm, "--haltcc", "--mode", "JTAG",
                                   "--operation", "P;" + bitstream_filename])


if __name__ == "__main__":
    from .test.blinky import Blinky

    DE2115Platform().build(Blinky(), do_program=True)
