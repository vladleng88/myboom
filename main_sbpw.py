from lib.atmosphere import Atmosphere
from lib.params import Params
from lib.raytrace import Raytrace
from lib.aerodynamics import Aerodynamics
from lib.aerodynamics_sbpw import AerodynamicsSBPW
from lib.pathway import Pathway
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import *
from lib.praphview import *

atmosphere = Atmosphere(r'in/sbpw_atm/air.dat')
atmosphere.setAtmoshere()

#-------------Enter tetta angle------------------
tetta = 70
#-------------End tetta angle------------------

#windPathPlot(list(atmosphere.getDefaultHeight().values()), list(atmosphere.getDefaultWindX().values()), list(atmosphere.getDefaultWindY().values()), list(atmosphere.getDefaultWindZ().values()))
params = Params(16459.2-82.296, 0, 0, 0, 0, 0, 1.4, 110.011306632, 91625, 27.432)
a = {'ax': 0, 'ay': 0, 'az': 0}
dVdh = {'dVdhx': 0, 'dVdhy': 0, 'dVdhz': 0}
dadh = {'dadhx': 0, 'dadhy': 0, 'dadhz': 0}
raytrace = Raytrace(tetta, params, atmosphere, a, dadh, dVdh)
aerodynamics = AerodynamicsSBPW(params, raytrace.getFlightMachNumber(), r'in/sbpw_atm/case2_'+str(tetta)+'.txt')
coeff_normal = 0.5*atmosphere.getDensity(params.getY0())*(raytrace.getFlightMachNumber()**2)*\
    (raytrace.soundSpeed(atmosphere.getTemperature(params.getY0())))**2*sqrt(params.getLength())/\
    (sqrt((raytrace.getFlightMachNumber())**2 - 1)*params.getLift())
#print(sqrt((raytrace.getFlightMachNumber())**2 - 1))
#print('coeff_normal=', coeff_normal)
aerodynamics.setAerodynmamicsData(coeff_normal)
ettaRef = aerodynamics.getEttaRef()
withemRef = aerodynamics.getWithemRef()
potentialRef = aerodynamics.getPotentalRef()
dSdX = aerodynamics.getdSdX()
print('ettaRef', len(ettaRef))
print('dSdX', len(dSdX))

P_BANG = {}; T_BANG = {}
FF_DOP = {}; T_DOP = {}
xx = []; yy = []; zz = []
k = 0; k1 = 0; k2 = 0
y_rev = 0
y=params.getY0()
dt = raytrace.getDt()
t = params.gett0()
x = params.getX0()
z = params.getZ0()
xx.append(x)
yy.append(y)
zz.append(z)
ny = raytrace.getNoy()
y_next = y+raytrace.getDy(y, ny)
Integrals = raytrace.getInitialIntagrals()
I1 = Integrals['I1']
I2 = Integrals['I2']
I3 = Integrals['I3']
I4 = Integrals['I4']
print('ny_start', ny)
print('I1_start', I1)
print('I2_start', I2)
print('I3_start', I3)
print('I4_start', I4)
i1_test = I1
M_eff = 1/sqrt(1-ny**2)
while y >= params.getYtarget() and y_next >= params.getYtarget():
    dy = raytrace.getDy(y, ny)
    y_rev = y_rev + dy
    y = params.getY0() + y_rev
    ny_next = raytrace.n_definition(y, ny)['ny']
    dy_next = raytrace.getDy(y, ny_next)
    y_rev_next = y_rev + dy_next
    y_next = params.getY0() + y_rev_next
    #print('y', y, 'dy', dy, 'ynext', y_next)
    if y_next >= params.getYtarget():
        x = x + raytrace.getDx(y, ny, dy_next)
        xx.append(x)
        z = z + raytrace.getDz(y, ny, dy_next)
        zz.append(z)
        yy.append(y)
        t = t + dt
    else:
        #dy = y - dy
        dy = y-params.getYtarget() - dy
        y = params.getYtarget()
        u_final = atmosphere.getWindY(y)+raytrace.soundSpeed(atmosphere.getTemperature(y))*raytrace.n_definition(y,ny)['ny']
        dt_final = dy/u_final
        x = x + raytrace.getDx(y, ny, dy)
        z = z + raytrace.getDz(y, ny, dy)
        t = t + dt_final
        xx.append(x)
        zz.append(z)
        yy.append(y)
    print('x=', x, 'y=', y, 'z=', z)
    Integrals = raytrace.getDIntegrals(y, ny, dy)
    I1 = I1 + Integrals['dI1']
    I2 = I2 + Integrals['dI2']
    I3 = I3 + Integrals['dI3']
    I = raytrace.getIntegral(I1, I2, I3)
    I4 = I4 + raytrace.getDIntegral4(y, ny, I, dy)
    #k = raytrace.getK(I4)
    #k1 = raytrace.getK1(params.getYtarget(), I, ny)
    #k2 = raytrace.getK2()
    ny = raytrace.n_definition(y, ny)['ny']

    #print('h=', y, 'I1=', I1,'I2=', I2,'I3=', I3,'I4=', I4, 'I', I)
    #print('h=', y, ' k=', k, ' k1=', k1, ' k2=', k2, 'I1=', I1,'I2=', I2,'I3=', I3,'I4=', I4, 'I', I)
    #i1_test += (raytrace.soundSpeed(atmosphere.getTemperature(y)))*dy/ny
    #print('h=', y, ' k=', k, ' k1=', k1, ' k2=', k2, 'I1=', I1, 'ny', ny, 'a', raytrace.soundSpeed(atmosphere.getTemperature(y)), 'i1_test', i1_test)
k = raytrace.getK(I4)
k1 = raytrace.getK1(params.getYtarget(), I, ny)
k2 = raytrace.getK2()
print(' k=', k, ' k1=', k1, ' k2=', k2, )
print('l=',params.getLength(), 'a0=', raytrace.soundSpeed(atmosphere.getTemperature(16459.2-82.296)), 'M=', raytrace.getFlightMachNumber())
print('sigma', raytrace.getSigma())
print('gamma', raytrace.getGamma())
for j in range(0, len(withemRef)):
   FF_DOP[j] = 2*potentialRef[j]/k - withemRef[j]**2
   T_DOP[j] = ettaRef[j] - k*withemRef[j]
#Take the minimum and maximum value of the duration
T_MIN = T_DOP[0]
T_MAX = T_DOP[0]
for j in range(0, len(withemRef)):
    if T_MIN > T_DOP[j]:
        T_MIN = T_DOP[j]
    if T_MAX < T_DOP[j]:
        T_MAX = T_DOP[j]
DT = (T_MAX - T_MIN)/(params.getIspace()-1)
P_BOOM = {}
T_BOOM = {}
P_HALF_BOOM = {}
nPT = 1
T = {}
FF_wave = {}
F_wave = {}
print('T_MIN=', T_MIN, ' T_MAX=', T_MAX)
print('DT = ', DT)
for j in range(0, (params.getIspace())):
    T[j] = T_MIN + (j)*DT
    #FF_wave[j] = 0
F_wave[0] = 0
count = 0
t_start = 0
for i in range(1, len(withemRef)):
    for j in range(0, len(T)):
        if T[j]>=T_DOP[i-1] and T[j]<T_DOP[i]:
            a = (withemRef[i]-withemRef[i-1])/(ettaRef[i] - ettaRef[i-1])
            b = withemRef[i-1] + 2 * (potentialRef[i] - potentialRef[i-1])/(ettaRef[i] - ettaRef[i-1]) - withemRef[i]
            FF = FF_DOP[i-1] + (T[j] - T_DOP[i-1]) * (b - 2*a*k*withemRef[i-1] + a*(T[j] - T_DOP[i-1]))/(k * (1-a*k))
            if t_start == 0:
                t_start = T[j]
            if FF_wave.get(T[j]) or FF_wave.get(T[j]) == 0:
                if FF > FF_wave[T[j]]:
                    FF_wave[T[j]] = FF
            else:
                FF_wave[T[j]] = FF
TT = sorted(list(FF_wave.keys()))
ttt = {}
FFF = {}
counter = 0
#print(len(TT))
#for tt in TT:
#    if tt<t_start:
#        FF_wave[tt] = 0
#counter = 0
for tt in TT:
    if tt>=t_start and tt<2.7:
        FFF[counter] = FF_wave[tt]
        ttt[counter] = tt
        counter+=1
        #print(tt, '\t', FF_wave[tt])
print('t_start', t_start)

F_wave[0] = 0
for i in range(1, len(FFF)):
    F_wave[i] = (k/2)*(FFF[i] - FFF[i - 1]) / (ttt[i] - ttt[i - 1])

for j in range(0, len(F_wave)):
    P_BOOM[j] = k1*F_wave[j]*1.9
    T_BOOM[j] = k2*(ttt[j])
    #print('j',j ,'\t', 'etta=', ettaRef[j], '\t','t=', T_BOOM[j], '\t','p=', P_BOOM[j])
print('len_TBoom', len(T_BOOM))
print('len_PBoom', len(P_BOOM))
graphPlot(ettaRef, dSdX, potentialRef, withemRef, T_BOOM, P_BOOM,  T_DOP, FF_DOP, ttt, FFF, raytrace.getTetta())
#graphPlotSBPW(ettaRef,dSdX, withemRef, T_BOOM, P_BOOM,  T_DOP, FF_DOP, ttt, FFF, i=1)
#flatPathPlot(xx, yy, zz)
#windPathPlot(atmosphere.getDefaultWindX(), atmosphere.getDefaultWindY(), atmosphere.getDefaultWindZ())
spacedPathPlot(xx, yy, zz, raytrace.getTetta())
res = open(r'res/res_sbpw_'+str(raytrace.getTetta())+'.txt', 'w', encoding='utf-8' )
for i in range(0, len(T_BOOM)):
    res.write('\t'+str(list(T_BOOM.values())[i])+'\t'+str(list(P_BOOM.values())[i])+'\n')

