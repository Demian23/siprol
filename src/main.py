import numpy as n
import matplotlib.pyplot as plt
import sounddevice as sa
from ui.cmdl import CmdlUI, Request 
from sig.interface import Signal


def main():
    ui = CmdlUI()
    request: Request = ui.process()
    rate = request.sample_rate
    duration = request.seconds_duration
    sig: Signal = request.signal
    time = n.arange(0, duration * rate) / rate 
    sig_val = [sig.at(t) for t in time]
    if request.view:
        plt.xlabel('Time')
        plt.ylabel('Sin')
        plt.plot(time[:500], sig_val[:500])
        plt.show()
    if request.sound:
        sa.play(sig_val, rate, blocking=True)

main()
