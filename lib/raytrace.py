from math import *
from lib.atmosphere import Atmosphere
from lib.params import Params


class Raytrace:

    def __init__(self, fi, params: Params, atmosphere: Atmosphere, a):
        self.__fi = fi
        self.__params = params
        self.__atmosphere = atmosphere
        #self.__nox = self.__nox_definition()
        #self.__noy = self.__noy_definition()
        #self.__noz = self.__noz_definition()
        self.__dt = 0.05
        self.__a = a


    def __nox_definition(self):
        omega = self.__params.getOmega()
        omega1 = self.__params.getOmega1()
        myu = self.getMyu()
        nox = 0
        return nox

    def __noy_definition(self):
        omega = self.__params.getOmega()
        myu = self.getMyu()
        noy = 0
        return noy

    def __noz_definition(self):


        noz = 0
        return noz

    def getGamma(self):
        lyanda = sqrt(self.getFlightMachNumber()**2-1)
        gamma = asin(lyanda*sin(radians(self.__fi))/sqrt(1+(lyanda*sin(radians(self.__fi)))**2))
        print(self.__fi)
        return gamma

    def n_definition(self, y, ny_prev=-1):
        n = {}
        nox = self.getNox()
        noy = self.getNoy()
        noz = self.getNoz()
        T0 = self.__atmosphere.getTemperature(self.__params.getY0())
        dWindX = self.__atmosphere.getWindX(y) - self.__atmosphere.getWindX(self.__params.getY0())
        dWindZ = self.__atmosphere.getWindZ(y) - self.__atmosphere.getWindZ(self.__params.getY0())
        a = self.soundSpeed(self.__atmosphere.getTemperature(y))
        a_star = self.soundSpeed(T0) + self.__atmosphere.getWindY(self.__params.getY0()) * noy - \
                 (dWindX * nox + dWindZ * noz)
        # Вычисление коэффициентов квадратного уравнения для определения ny
        c0 = (1 - noy ** 2) * (self.__atmosphere.getWindY(y)) ** 2 + a_star ** 2
        c1 = 2 * (1 - noy ** 2) * (self.__atmosphere.getWindY(y)) * a
        c2 = (1 - noy ** 2) * (a) ** 2 - a_star ** 2
        #print('y=', y, 'd=', c1 ** 2 - 4 * c0 * c2)
        d = sqrt(c1 ** 2 - 4 * c0 * c2)
        ny1 = (-1 * c1 + d) / (2 * c0)
        ny2 = (-1 * c1 - d) / (2 * c0)
        if ny1*ny_prev > 0:
            n['ny'] = ny1
        elif ny2*ny_prev > 0:
            n['ny'] = ny2
        else:
            exit('Ошибка с определнием ny')
        nx = nox * (a + self.__atmosphere.getWindY(y) * n['ny']) / a_star
        n['nx'] = nx
        nz = noz * (a + self.__atmosphere.getWindZ(y) * n['ny']) / a_star
        n['nz'] = nz
        return n



    def getNox(self):
        return self.__nox

    def getNoy(self):
        return self.__noy

    def getNoz(self):
        return self.__noz

    def getDt(self):
        return self.__dt

    def getFlightMachNumber(self):
        y0 = self.__params.getY0()
        omega = self.__params.getOmega()
        omega1 = self.__params.getOmega1()
        T0 = self.__atmosphere.getTemperature(y0)
        M0 = self.__params.getMachNumber0()
        V = M0 * self.soundSpeed(T0)
        Vx = V * cos(radians(omega)) * cos(radians(omega1))
        Vy = V * sin(radians(omega))
        Vz = V * cos(radians(omega)) * sin(radians(omega1))
        windX = self.__atmosphere.getWindX(y0)
        windY = self.__atmosphere.getWindY(y0)
        windZ = self.__atmosphere.getWindZ(y0)
        dVx = Vx + windX
        dVy = Vy + windY
        dVz = Vz + windZ
        V_new = sqrt(dVx ** 2 + dVy ** 2 + dVz ** 2)
        M = V_new / self.soundSpeed(T0)
        #return M
        return self.__params.getMachNumber0()

    def getMyu(self):
        myu = degrees(asin(1 / self.getFlightMachNumber()))
        return myu

    def getDy(self, y, ny_prev):
        return (self.__atmosphere.getWindY(y) + self.soundSpeed(self.__atmosphere.getTemperature(y))*self.n_definition(y, ny_prev)['ny']) * self.getDt()

    def getDx(self, y, ny_prev, dy_next):
        n = self.n_definition(y, ny_prev)
        T = self.__atmosphere.getTemperature(y)
        Vy = self.__atmosphere.getWindY(y)
        k1 = (self.__atmosphere.getWindX(y)) + self.soundSpeed(T) * n['nx']
        #dy_half_h = (self.soundSpeed(T) * n['ny'] + Vy) * self.getDt()/2
        dy_half_h = dy_next/2
        k2 = (self.__atmosphere.getWindX(fabs(y + dy_half_h))) + self.soundSpeed(self.__atmosphere.getTemperature(fabs(y + dy_half_h))) * n['nx']
        k3 = (self.__atmosphere.getWindX(fabs(y + dy_half_h))) + self.soundSpeed(self.__atmosphere.getTemperature(fabs(y + dy_half_h))) * n['nx']
        #dy_h = (self.soundSpeed(T) * n['ny'] + Vy) * self.getDt()
        dy_h = dy_next
        k4 = (self.__atmosphere.getWindX(fabs(y + dy_h))) + self.soundSpeed(self.__atmosphere.getTemperature(y + dy_h)) * n['nx']
        dx = self.getDt()*(k1+2*k2+2*k3+k4)/6
        return dx

    def getDz(self, y, ny_prev, dy_next):
        n = self.n_definition(y, ny_prev)
        T = self.__atmosphere.getTemperature(y)
        Vy = self.__atmosphere.getWindY(y)
        k1 = (self.__atmosphere.getWindZ(y)) + self.soundSpeed(T) * n['nz']
        #dy_half_h = (self.soundSpeed(T) * n['ny'] + Vy) * self.getDt()/2
        dy_half_h = dy_next / 2
        k2 = (self.__atmosphere.getWindZ(fabs(y + dy_half_h))) + self.soundSpeed(self.__atmosphere.getTemperature(fabs(y + dy_half_h))) * n['nz']
        k3 = (self.__atmosphere.getWindZ(fabs(y + dy_half_h))) + self.soundSpeed(self.__atmosphere.getTemperature(fabs(y + dy_half_h))) * n['nz']
        #dy_h = (self.soundSpeed(T) * n['ny'] + Vy) * self.getDt()
        dy_h = dy_next
        k4 = (self.__atmosphere.getWindZ(fabs(y + dy_h))) + self.soundSpeed(self.__atmosphere.getTemperature(fabs(y + dy_h))) * n['nz']
        dz = self.getDt()*(k1+2*k2+2*k3+k4)/6
        return dz

    def soundSpeed(self, T):
        return sqrt(self.__params.getKappa() * self.__params.getR() * T)
