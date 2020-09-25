from lib.params import Params
from math import *

class AerodynamicsSBPW:

    def __init__(self, params: Params, MachNumber, path=r'in/sbpw_atm/case2_0.txt', Ngeoam = 4048):
        self.__path = path
        self.__withemRef = {}
        self.__cp = {}
        self.__ettaRef = {}
        self.__potentialRef = {}
        self.__Ngeom = Ngeoam
        self.__params = params
        self.__MachNumber = MachNumber

    def setAerodynmamicsData(self, k111):
        input = self.getInputData()
        inputResample = self.getResampleInputData(input)
        const = (self.__MachNumber ** 2 * self.__params.getKappa()) / (
                    2 * pi * self.__params.getLength() * sqrt(2 * sqrt(self.__MachNumber ** 2 - 1)))
        self.__ettaRef = inputResample['ettaRefResample']
        print('const', const)
        for i in range(0, len(inputResample['cpResample'])):
            self.__cp[i] = inputResample['cpResample'][i]

        self.__potentialRef[0] = 0
        self.__withemRef[0] = 0

        betta = sqrt(self.__MachNumber ** 2 - 1)
        r = 82.296

        for i in range(1, len(self.__cp)):
            potential_integral = 0
            for j in range(0, i):
                if self.__ettaRef[j] > 3:
                    continue
                potential_loc = pi * sqrt(2 * betta * r) * 0.5 * (self.__cp[j] + self.__cp[j + 1]) * (
                            self.__ettaRef[j + 1] - self.__ettaRef[j]) * self.__params.getLength()
                potential_integral = potential_integral + potential_loc
            self.__potentialRef[i] = k111 * potential_integral

        for i in range(1, len(self.__cp) - 1):
            withem_loc = (self.__potentialRef[i + 1] - self.__potentialRef[i - 1]) / (
                        self.__ettaRef[i + 1] - self.__ettaRef[i - 1])
            # print(withem_loc)
            # count += 1
            if self.__ettaRef[i] < 0:
                self.__withemRef[i] = 0
            else:
                self.__withemRef[i] = withem_loc
        self.__withemRef[len(self.__cp) - 1] = 0


    def getInputData(self):
        file = open(self.__path, 'r', encoding='utf-8')
        cp = {}
        ettaRef = {}

        # position = int(file.read().find('@'))
        # file.seek(position)
        for line in file:
            if line[len(line) - 2] == '@':
                break
        count = 1
        for line in file:
            list = line.split('\t')
            # print(list)
            # if float(list[0]) < 0.0:
            #    continue
            if float(list[0]) > 3:
                break
            ettaRef[count] = float(list[0])
            cp[count] = float(list[1])
            count += 1
        ettaRef[0] = ettaRef[1] - 0.5
        cp[0] = 0
        print('etta_before', len(ettaRef))
        print('cp_before', len(cp))
        return {'ettaRef': ettaRef, 'cp': cp}

    def getWithemRef(self):
        return self.__withemRef

    def getCp(self):
        return self.__cp

    def getEttaRef(self):
        return self.__ettaRef
    def getPotentalRef(self):
        return self.__potentialRef

    def getResampleInputData(self, input):
        ettaRef = input['ettaRef']
        cp = input['cp']
        Ka = {}
        Kb = {}
        for i in range(0, len(cp) - 1):
            Ka[i] = (cp[i + 1] - cp[i]) / (ettaRef[i + 1] - ettaRef[i])
            Kb[i] = (cp[i] * ettaRef[i + 1] - cp[i + 1] * ettaRef[i]) / (ettaRef[i + 1] - ettaRef[i])
        Xgeom = ettaRef[len(ettaRef) - 1] - ettaRef[0]
        dx = (Xgeom) / (self.__Ngeom - 1)
        ettaRefResample = {}
        cpResample = {}
        # c=0
        for j in range(0, self.__Ngeom):
            ettaRefResample[j] = ettaRef[0] + j * dx
        for i in range(0, len(cp) - 1):
            for j in range(0, self.__Ngeom):
                if (ettaRefResample[j] >= ettaRef[i] and ettaRefResample[j] <= ettaRef[i + 1]):
                    cpResample[j] = Ka[i] * ettaRefResample[j] + Kb[i]
                    # print('count', c,'min', ettaRef[i], 'max',ettaRef[i+1], '\tetta=', ettaRefResample[j], '\t', dSdXResample[j])
                    # c+=1
                # if ettaRefResample[j] == ettaRef[i+1]:
                #    dSdXResample[j] = Ka[i] * ettaRefResample[j] + Kb[i]
                #    print('count', c, 'min', ettaRef[i], 'max', ettaRef[i + 1], '\tetta=', ettaRefResample[j], '\t',
                #          dSdXResample[j])
        # print(len(ettaRefResample))
        # print(len(dSdXResample))
        # for i in range(0, len(ettaRefResample)):
        # print('i', i, 'etta', ettaRefResample[i], 'ds_dx =', dSdXResample[i])

        # print('etta_after', len(ettaRefResample))
        # print('dSdX_after', len(dSdXResample))
        # print('etta_final', ettaRef[len(dSdX)-1])
        # print('etta_res_final', ettaRefResample[self.__Ngeom-1])
        return {'ettaRefResample': ettaRefResample, 'cpResample': cpResample}


