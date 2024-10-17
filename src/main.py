import numpy as n
import matplotlib.pyplot as plt
import sounddevice as sa
import soundfile as sf
from ui.cmdl import CmdlUI, Request 
from dsp.sig import Signal
from dsp.ft import FourierTransformation


def main():
    ui = CmdlUI()
    request: Request = ui.process()
    rate = request.sample_rate
    duration = request.seconds_duration
    sig: Signal = request.signal
    time = n.linspace(0, int(duration * rate), int(duration * rate), endpoint=False) / rate 
    sig_val = [sig.at(t) for t in time]
    if request.view:
        plt.xlabel('Time')
        plt.ylabel('Sig')
        plt.plot(time, sig_val)
        plt.show()
    if request.sound:
        sa.play(sig_val, rate, blocking=True);
    if request.draw_spectrum:
        ft = FourierTransformation(sig_val, time)
        ft.correlational()
        plt.figure(figsize=(16, 10))
        plt.subplot(221)
        plt.stem(ft.Re, basefmt='C3')
        plt.subplot(222)
        plt.stem(ft.Im, basefmt='C3')
        plt.subplot(223)
        plt.stem(ft.magnitude(), basefmt='C3')
        plt.grid(True)
        plt.subplot(224)
        plt.stem(ft.phase(), basefmt='C3')
        plt.grid(True)
        plt.show()

main()
