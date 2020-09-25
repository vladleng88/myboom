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
fi = 10 #fi
#-------------End tetta angle------------------

#windPathPlot(list(atmosphere.getDefaultHeight().values()), list(atmosphere.getDefaultWindX().values()), list(atmosphere.getDefaultWindY().values()), list(atmosphere.getDefaultWindZ().values()))
params = Params(16459.2-82.296, 0, 0, 0, 0, 0, 1.4, 110.011306632, 91625, 27.432)
a = {'ax': 0, 'ay': 0, 'az': 0}
raytrace = Raytrace(fi, params, atmosphere, a)
aerodynamics = AerodynamicsSBPW(params, raytrace.getFlightMachNumber(), r'in/sbpw_atm/case2_'+str(fi)+'.txt')
coeff_normal = 0.5*atmosphere.getDensity(params.getY0())*(raytrace.getFlightMachNumber()**2)*\
    (raytrace.soundSpeed(atmosphere.getTemperature(params.getY0())))**2*sqrt(params.getLength())/\
    (sqrt((raytrace.getFlightMachNumber())**2 - 1)*params.getLift())
#print(sqrt((raytrace.getFlightMachNumber())**2 - 1))
print('coeff_normal=', coeff_normal)
#aerodynamics.setAerodynmamicsData(coeff_normal)
gamma = raytrace.getGamma()
print('damma', degrees(gamma))