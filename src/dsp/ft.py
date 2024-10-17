import numpy as np

class FourierTransformation:

    def __init__(self, signal, time):
        self.__s = signal
        self.__t = time
        N = len(signal)
        self.fr_count = int(N / 2) + 1
        self.Re = np.zeros(self.fr_count)
        self.Im = np.zeros(self.fr_count)

    def correlational(self):
        '''Correlational, or net method for Fourier Transformation'''
        '''In rectangle coordinate system'''
        pi2 = np.pi * 2
        #time here already devided on sample rate
        for frequency in range(self.fr_count):
            self.Re[frequency] = sum(self.__s * np.cos(pi2 * frequency * self.__t))
            self.Im[frequency] = -sum(self.__s * np.sin(pi2 * frequency * self.__t))

    def magnitude(self):
        return np.sqrt(self.Re ** 2 + self.Im ** 2)

    def phase(self):
        phase = np.zeros(self.fr_count)
        for frequency in range(self.fr_count):

            if self.Re[frequency] != 0:
                phase[frequency] = np.arctan2(self.Im[frequency], 
                                              self.Re[frequency])
            else:
                if self.Im[frequency] > 0:
                    phase[frequency] = np.pi / 2
                else: 
                    phase[frequency] = -np.pi / 2


            if self.Re[frequency] < 0:
                if self.Im[frequency] < 0:
                    phase[frequency] -= np.pi
                else: 
                    phase[frequency] += np.pi
        return phase
