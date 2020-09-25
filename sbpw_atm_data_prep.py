from math import *
fileT = open(r'in/sbpw_atm/profileT.dat', 'r', encoding='utf-8')
profileT = {}
count = 0
for line in fileT:
    listt = line.split(' ')
    key = float(listt[0])
    profileT[key] = float(listt[1])
fileT.close()

fileT = open(r'in/sbpw_atm/profileP.dat', 'r', encoding='utf-8')
profileP = {}
count = 0
for line in fileT:
    listt = line.split(' ')
    key = float(listt[0])
    profileP[key] = float(listt[1])
fileVx = open(r'in/sbpw_atm/windX.dat', 'r', encoding='utf-8')
profileVx = {}
count = 0
for line in fileVx:
    listt = line.split(' ')
    key = float(listt[0])
    profileVx[key] = float(listt[1])
fileVz = open(r'in/sbpw_atm/windZ.dat', 'r', encoding='utf-8')
profileVz = {}
count = 0
for line in fileVz:
    listt = line.split(' ')
    key = float(listt[0])
    profileVz[key] = float(listt[1])
print(profileT)
print(profileP)
print(profileVx)
print(profileVz)
print(len(profileT))
print(len(profileP))
print(len(profileVx))
print(len(profileVz))

h = list(profileT.keys())
T = list(profileT.values())
Vx = list(profileVx.values())
Vz = list(profileVz.values())
P = list(profileP.values())
air = open(r'in/sbpw_atm/air.dat', "a",  encoding='utf-8')
for i in range(0, len(profileT)):
    air.write("\t"+str(h[i])+"\t"+str(T[i]+273)+"\t"+str(Vx[i])+"\t"+str(0)+"\t"+str(-1*Vz[i])+"\t"+str(P[i]/287.3/(T[i]+273))+"\n")
