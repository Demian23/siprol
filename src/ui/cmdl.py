import argparse
from sig.interface import DefaultAmplitude, DefaultPhase, Signal
from sig.impl import AmplitudeModulation, FrequencyModulation, RectanglePulse, Sawtooth, Sinus, Sum, Triangle, Noise

class Request:
    def __init__(self, signal: Signal, sample_rate: int, view: bool, sound: bool, seconds_duration: int):
        self.signal = signal
        self.view = view
        self.sound = sound
        self.seconds_duration = seconds_duration
        self.sample_rate = sample_rate 

class CmdlUI:

    def __init__(self, 
                 permited_operations=['run', 'sum', 'amplitude_modulation', 'frequency_modulation'],
                 permited_signals=['sin', 'pulse', 'triangle', 'sawtooth', 'noise'],
                 app_description="Tool for signal processing and generation"):

        parser = argparse.ArgumentParser(description=app_description)
        parser.add_argument('--operation', required=True, 
                            choices=permited_operations,
                            help="Type of operation")
        parser.add_argument('--sample_rate', required=True, 
                            type=int,
                            help="Sample rate")
        parser.add_argument('--amplitude', nargs='+', type=float, help='Amplitude of the signal')
        parser.add_argument('--frequency', nargs='+', type=float,  help='Frequency of the signal in Hz')
        parser.add_argument('--phase_shift', nargs='+', type=float, help='Phase shift of the signal in radians')
        parser.add_argument('--duration', type=float,  help='Duration of the signal in seconds')
        parser.add_argument('--sound', action='store_true', help='Listen generated signal')
        parser.add_argument('--duty_cycle', nargs='+', type=float, help='For pulse')
        parser.add_argument('--view', action='store_true', help='View graphics')
        parser.add_argument('--signals', nargs='+', choices=permited_signals)
        self.__parser = parser

    def read_signal(self, parsed_values, sig) -> Signal:
        phase = DefaultPhase(parsed_values.frequency.pop(0), parsed_values.phase_shift.pop(0))
        ampl = DefaultAmplitude(parsed_values.amplitude.pop(0))
        match sig:
            case 'sin':
                return Sinus(phase, ampl)
            case 'pulse':        
                return RectanglePulse(phase, ampl, parsed_values.duty_cycle.pop(0))
            case 'triangle':
                return Triangle(phase, ampl)
            case 'sawtooth':        
                return Sawtooth(phase, ampl)
            case 'noise':        
                return Noise(phase, ampl)
            case _:
               raise ValueError() 

    def read_all_signals(self, parsed_values):
        size = len(parsed_values.signals)
        signals = []
        for x in range(size):
            signals.append(
                    self.read_signal(parsed_values, parsed_values.signals[x]))
        return signals

        

    def process(self):
        parsed = self.__parser.parse_args()
        sig: Signal
        signals = self.read_all_signals(parsed)
        match parsed.operation:
            case 'run':
                sig = signals[0] 
            case 'sum':
                sig = Sum(signals[0], signals[1])
            case 'amplitude_modulation':
                sig = AmplitudeModulation(signals[0], signals[1])
            case 'frequency_modulation':
                sig = FrequencyModulation(signals[0], signals[1], parsed.sample_rate)
            case _:
               raise ValueError() 
        return Request(sig, parsed.sample_rate, parsed.view, parsed.sound, 
                       parsed.duration)
