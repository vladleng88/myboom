from math import *

class Params:

    def __init__(self, y0=15500,#метров
                 x0=0,
                 z0=0,
                 t0=0,
                 omega=0,
                 omega1=0,
                 M0=1.7,
                 y_target=0,
                 lift=15000*9.81,# N
                 length=30.346,#метров
                 kappa=1.4,
                 R=287.3,
                 ispace=4000
                 ):
        self.__y0 = y0
        self.__x0 = x0
        self.__z0 = z0
        self.__t0 = t0
        self.__omega = omega
        self.__omega1 = omega1
        self.__M0 = M0
        self.__R = R
        self.__kappa = kappa
        self.__lift = lift
        self.__length = length
        self.__y_target = y_target
        self.__ispace = ispace

    def getMachNumber0(self):
        return self.__M0
    def setMachNumber0(self, M0):
        self.__M0 = M0

    def getOmega(self):
        return self.__omega
    def setOmega(self, omega):
        self.__omega = omega

    def getOmega1(self):
        return self.__omega1
    def setOmega1(self, omega1):
        self.__omega1 = omega1

    def getKappa(self):
        return self.__kappa
    def setKappa(self, kappa):
        self.__kappa = kappa

    def getR(self):
        return self.__R
    def setR(self, R):
        self.__R = R

    def getX0(self):
        return self.__x0
    def setX0(self, x0):
        self.__x0 = x0

    def getY0(self):
        return self.__y0
    def setY0(self, y0):
        self.__y0 = y0

    def getZ0(self):
        return self.__z0
    def setZ0(self, z0):
        self.__z0 = z0

    def gett0(self):
        return self.__t0
    def sett0(self, t0):
        self.__t0 = t0

    def getLift(self):
        return self.__lift
    def setLift(self, lift):
        self.__lift = lift

    def getLength(self):
        return self.__length
    def setLength(self, length):
        self.__length = length

    def getYtarget(self):
        return self.__y_target
    def setYtarget(self, y_target):
        self.__y_target = y_target

    def getIspace(self):
        return self.__ispace
    def setIspace(self, ispace):
        self.__ispace = ispace
