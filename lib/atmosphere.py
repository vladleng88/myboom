

class Atmosphere:
    __path = ''
    __H = {}
    __T = {}
    __Vx = {}
    __Vy = {}
    __Vz = {}
    __d = {}

    def __init__(self, path=r'in/air.dat'):
        self.__path = path

    def setAtmoshere(self):
        file = open(self.__path, 'r', encoding='utf-8')
        # position = int(file.read().find('@'))
        # file.seek(position)
        for line in file:
            if line[len(line)-2] == '@':
                break
        count = 1
        for line in file:
            list = line.split()
            self.__H[count] = float(list[0])
            self.__T[count] = float(list[1])
            self.__Vx[count] = float(list[2])
            self.__Vy[count] = float(list[3])
            self.__Vz[count] = float(list[4])
            self.__d[count] = float(list[5])
            count += 1

    def __getDefaultHeight(self):
        return self.__H
    def __getDefaultTemperature(self):
        return self.__T
    def __getDefaultWindX(self):
        return self.__Vx
    def __getDefaultWindY(self):
        return self.__Vy
    def __getDefaultWindZ(self):
        return self.__Vz
    def __getDefaultDensity(self):
        return self.__d
    def __getHmax(self):
        max = 0
        for key in self.__H:
            if max < self.__H[key]:
                max = self.__H[key]
        return max
    def getTemperature(self, y0):
        for key in self.__getDefaultHeight():
            if y0 >= self.__getDefaultHeight()[key] and y0 < self.__getDefaultHeight()[key+1]:
                temp = self.__getDefaultTemperature()[key]
        return temp
    def getWindX(self, y0):
        for key in self.__getDefaultHeight():
            if y0 >= self.__getDefaultHeight()[key] and y0 < self.__getDefaultHeight()[key+1]:
                temp = self.__getDefaultWindX()[key]
        return temp
    def getWindY(self, y0):
        for key in self.__getDefaultHeight():
            if y0 >= self.__getDefaultHeight()[key] and y0 < self.__getDefaultHeight()[key+1]:
                temp = self.__getDefaultWindY()[key]
        return temp
    def getWindZ(self, y0):
        for key in self.__getDefaultHeight():
            if y0 >= self.__getDefaultHeight()[key] and y0 < self.__getDefaultHeight()[key+1]:
                temp = self.__getDefaultWindZ()[key]
        return temp
    def getDensity(self, y0):
        for key in self.__getDefaultHeight():
            if y0 >= self.__getDefaultHeight()[key] and y0 < self.__getDefaultHeight()[key+1]:
                temp = self.__getDefaultDensity()[key]
        return temp


