import numpy as m

pi2 = m.pi * 2

class DefaultAmplitude:

    def __init__(self, amplitude):
        self.amplitude = amplitude

    def __call__(self, t):
        del t
        return self.amplitude

class DefaultPhase:

    def __init__(self, frequency, phase_shift):
        self.frequency = frequency 
        self.phase_shift = phase_shift

    def __call__(self, t):
        return pi2  * self.frequency * t + self.phase_shift;

class Signal:
    '''TODO need to implement some sort of saving signal and it's params to file'''

    def __init__(self, phase_generator, amplitude_generator):
        '''Generators take one argument and return respectively amplitude or phase'''
        self._gen_ampl = amplitude_generator
        self._gen_phase = phase_generator 

    def at(self, x):
        '''x here number-like'''
        return self._gen_ampl(x) * self._gen_phase(x)
