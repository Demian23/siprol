from .interface import Signal, pi2
import numpy as m

class Noise(Signal):

    def at(self, x):
        return m.random.normal(0, 1) * self._gen_ampl(x) * self._gen_phase(x)

class Sinus(Signal):

    def at(self, x):
        return self._gen_ampl(x) * m.sin(self._gen_phase(x))

class RectanglePulse(Signal):
    
    def __init__(self, phase_generator, amplitude_generator, duty_cycle):
        Signal.__init__(self, phase_generator, amplitude_generator)
        self.__duty_cycle = duty_cycle

    def at(self, x):
        cond = self._gen_phase(x) % pi2 / pi2 <= self.__duty_cycle 
        ampl = self._gen_ampl(x)
        return ampl if cond else -ampl

class Triangle(Signal):

    def at(self, x):
        ampl = self._gen_ampl(x) * 2 / m.pi
        phase = self._gen_phase(x) 
        return ampl * (abs((phase + 3 * m.pi / 2) % pi2 - m.pi) - m.pi / 2) 


class Sawtooth(Signal):
    
    def at(self, x):
        ampl = self._gen_ampl(x)
        phase = self._gen_phase(x)
        return ampl /m.pi * ((phase + m.pi) % pi2 - m.pi)

class Sum(Signal):

    def __init__(self, A: Signal, B: Signal):
        self.__a = A
        self.__b = B

    def at(self, x):
        return self.__a.at(x) + self.__b.at(x) 

class AmplitudeModulation(Signal):

    def __init__(self, modulating: Signal, carrier: Signal):
        self.__modulating = modulating 
        self.__carrier = carrier
        old_ampl = self.__carrier._gen_ampl
        self.__carrier._gen_ampl = lambda t: old_ampl(t) * self.__modulating.at(t)
        

    def at(self, x):
        return self.__carrier.at(x) 

class FrequencyModulation(Signal):

    class __PhaseGenerator:
        def __init__(self, start_phase, old_frequency, modulator, sample_rate):
            self.start_phase = start_phase
            self.current_phase = 0
            self.old_frequency = old_frequency
            self.modulator = modulator
            self.sample_rate = sample_rate

        def __call__(self, t):
            if t == 0:
                self.current_phase = self.start_phase
            else:
                self.current_phase += pi2 * self.old_frequency * (1 + self.modulator(t)) / self.sample_rate
            return self.current_phase


    def __init__(self, modulating: Signal, carrier: Signal, sample_rate):
        self.__carrier = carrier
        self.__carrier._gen_phase = self.__PhaseGenerator(self.__carrier._gen_phase.phase_shift, self.__carrier._gen_phase.frequency, modulating.at, sample_rate)

    def at(self, x):
        return self.__carrier.at(x) 


'''
class FrequencyModulationSin(Signal):

    def __init__(self, carrier: Signal, modulating: Signal, modulation_sensivity): 
        self.__carrier = carrier
        self.__modulating = modulating
        self.__modulation_sensivity = modulation_sensivity

    def gen(self, X):
        m_val = self.__modulating.gen(X)
        fi = self.__carrier._fase_shift
        res = []
        for i in range(len(X)):
            res.append(m.sin(fi) * self.__carrier._amplitude)
            fi += pi2 * self.__carrier._frequency * ((1 + m_val[i])) / self.__modulation_sensivity
        return m.array(res)
        
class FrequencyModulationSawtooth(Signal):

    def __init__(self, carrier: Signal, modulating: Signal, modulation_sensivity): 
        self.__carrier = carrier
        self.__modulating = modulating
        self.__modulation_sensivity = modulation_sensivity

    def gen(self, X):
        m_val = self.__modulating.gen(X)
        fi = self.__carrier._fase_shift
        res = []
        for i in range(len(X)):
            res.append(self.__carrier._amplitude / m.pi * ((fi + m.pi) % (pi2) - m.pi))
            fi += pi2 * self.__carrier._frequency * ((1 + m_val[i])) / self.__modulation_sensivity
        return m.array(res)
        
'''
