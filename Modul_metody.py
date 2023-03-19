import numpy as np

#Moduł metody
class ICA(object):

    def __init__(self, signal_block, krok_uczenia):
        self.n = len(signal_block)
        self.X = np.array(signal_block)
        self.W = np.random.uniform(-0.0001, 0.0001, (self.n, self.n))
        self.y = np.matmul(self.W, self.X)
        self.G_y = 0
        self.F_y = 0
        self.krok_uczenia = krok_uczenia

    # Definicja funkcji  odpowiedzialnej za wykonanie algorytmu neutralnego gradientu dla separacji ślepej BSS
    def metoda_BSS(self, iteracions):
        for iteracion in range(iteracions):
            self.W += np.matmul(np.eye(self.n) - np.matmul(self.f(self.y), self.g(self.y)), self.krok_uczenia * self.W)
            self.y = np.matmul(self.W, self.X)
        return self.y

    @staticmethod
    def f(y):
        return y**3

    @staticmethod
    def g(y):
        return y.transpose()
