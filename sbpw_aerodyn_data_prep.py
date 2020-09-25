from lib.atmosphere import Atmosphere
from lib.praphview import *
tetta = -70
flightHeight = 16459.2
length = 27.432
MachNumber = 1.4
atm = Atmosphere(r'in/sbpw_atm/air.dat')
atm.setAtmoshere()
T = atm.getTemperature(flightHeight)
a = (1.4*287.3*T)**0.5
q = 0.5*atm.getDensity(flightHeight)*(MachNumber*a)**2
betta = (MachNumber**2-1)**0.5
print('T=', T, 'a=', a, 'q=', q, 'betta=', betta)
filePressure = open(r'in/sbpw_atm/pressure.txt', 'r', encoding='utf-8')
profilePressure = {}
for line in filePressure:
    listt = line.split(' ')
    key = float(listt[0])
    profilePressure[key] = float(listt[1])
p = list(profilePressure.values())
h = list(profilePressure.keys())
for i in range(0, len(p)):
    if flightHeight>h[i] and flightHeight<h[i+1]:
        a = (h[i+1] - h[i])/(p[i+1]-p[i])
        b = (h[i]*p[i+1] - h[i+1]*p[i])/(p[i+1]-p[i])
        p_flight = (flightHeight - b)/a
print('pressure=', p_flight)
file0 = open(r'in/sbpw_atm/pt_'+str(tetta)+'.txt', 'r', encoding='utf-8')
dSdX = {}
Cp = {}
x0 = {}
count = 0
for line in file0:
    listt = line.split()
    x0[count] = float(listt[0])
    Cp[count] = p_flight*(float(listt[1]))/q
    count+=1
file0.close()
print('lengthP0', len(Cp))
print('lengthx0', len(x0))
print(x0)
xmin = x0[0]
xmax = x0[0]
for i in range(0, len(x0)):
    if xmin>x0[i]:
        xmin = x0[i]
    if xmax<x0[i]:
        xmax = x0[i]
print('xmin=', xmin, 'xmax=', xmax)
xnorm0 = {}
Knorm = 1.5/(xmax-xmin)
for i in range(0, len(x0)):
    xnorm0[i] = (x0[i]-xmin)/length
print(xnorm0)
f0 = open(r'in/sbpw_atm/case2_'+str(tetta)+'.txt', 'w', encoding='utf-8')
for i in range(0, len(xnorm0)):
    f0.write(str(list(xnorm0.values())[i])+"\t"+str(list(Cp.values())[i])+"\n")
flatPlot(list(xnorm0.values()), list(Cp.values()))

