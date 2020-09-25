import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.ticker as ticker

def graphPlot(ettaRef, dSdX, potentialRef, withemRef, T_BOOM, P_BOOM, T_DOP, FF_DOP, ttt, FFF, i):
    fig, axs = plt.subplots(3, 2)

    axs[0, 0].plot(list(ettaRef.values()), list(dSdX.values()), linewidth=2.0, color='red')
    axs[0, 0].set_xlabel('etta')  # Add an x-label to the axes.
    axs[0, 0].set_ylabel('dS/dX')  # Add a y-label to the axes.

    axs[0, 1].plot(list(ettaRef.values()), list(potentialRef.values()), linewidth=2.0, color='red')
    axs[0, 1].set_xlabel('etta')  # Add an x-label to the axes.
    axs[0, 1].set_ylabel('Potential')  # Add a y-label to the axes.

    axs[2, 0].plot(list(ettaRef.values()), list(withemRef.values()), linewidth=2.0, color='red')
    axs[2, 0].set_xlabel('etta')  # Add an x-label to the axes.
    axs[2, 0].set_ylabel('Withem')  # Add a y-label to the axes.

    axs[1, 0].plot(list(T_DOP.values()), list(FF_DOP.values()), linewidth=2.0, color='red')
    axs[1, 0].plot(list(ttt.values()), list(FFF.values()), linewidth=2.0, color='blue')
    axs[1, 0].set_xlabel('t_wave')  # Add an x-label to the axes.
    axs[1, 0].set_ylabel('Ф_wave')  # Add a y-label to the axes.
    axs[1, 0].set_title("FFF_WAVE")  # Add a title to the axes.

    axs[1, 1].plot(list(T_BOOM.values()), list(P_BOOM.values()), linewidth=2.0, color='red')
    axs[1, 1].set_xlabel('t_boom')  # Add an x-label to the axes.
    axs[1, 1].set_ylabel('p_boom')  # Add a y-label to the axes.

    fig.savefig('res/figure'+str(i)+'.png')
    #plt.show()
    plt.close(fig)
def graphPlotSBPW(ettaRef,dSdX, withemRef, T_BOOM, P_BOOM, T_DOP, FF_DOP, ttt, FFF, i):
    fig, axs = plt.subplots(3, 2)

    axs[0, 0].plot(list(ettaRef.values()), list(dSdX.values()), linewidth=2.0, color='red')
    axs[0, 0].set_xlabel('etta')  # Add an x-label to the axes.
    axs[0, 0].set_ylabel('dS/dX')  # Add a y-label to the axes.

    axs[2, 0].plot(list(ettaRef.values()), list(withemRef.values()), linewidth=2.0, color='red')
    axs[2, 0].set_xlabel('etta')  # Add an x-label to the axes.
    axs[2, 0].set_ylabel('Withem')  # Add a y-label to the axes.

    axs[1, 0].plot(list(T_DOP.values()), list(FF_DOP.values()), linewidth=2.0, color='red')
    axs[1, 0].plot(list(ttt.values()), list(FFF.values()), linewidth=2.0, color='blue')
    axs[1, 0].set_xlabel('t_wave')  # Add an x-label to the axes.
    axs[1, 0].set_ylabel('Ф_wave')  # Add a y-label to the axes.
    axs[1, 0].set_title("FFF_WAVE")  # Add a title to the axes.

    axs[1, 1].plot(list(T_BOOM.values()), list(P_BOOM.values()), linewidth=2.0, color='red')
    axs[1, 1].set_xlabel('t_boom')  # Add an x-label to the axes.
    axs[1, 1].set_ylabel('p_boom')  # Add a y-label to the axes.

    fig.savefig('res/figure'+str(i)+'.png')
    #plt.show()
    plt.close(fig)

def dopPlotSBPW(T_DOP, FF_DOP, ttt, FFF, i):
    fig, ax = plt.subplots(figsize=(15,8))
    ax.plot(list(T_DOP.values()), list(FF_DOP.values()), linewidth=2.0, color='red')
    ax.plot(list(ttt.values()), list(FFF.values()), linewidth=2.0, color='blue')
    ax.set_xlabel('t_wave')  # Add an x-label to the axes.
    ax.set_ylabel('Ф_wave')  # Add a y-label to the axes.
    ax.set_title("FFF_WAVE")  # Add a title to the axes.
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.grid()
    plt.show()

def flatPathPlot(xx, yy , zz):
    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(xx, yy, linewidth=2.0, color='red')
    axs[0, 0].set_xlabel('x')
    axs[0, 0].set_ylabel('y')

    axs[0, 1].plot(zz, yy, linewidth=2.0, color='red')
    axs[0, 1].set_xlabel('z')
    axs[0, 1].set_ylabel('y')
    plt.show()

def spacedPathPlot(xx, yy, zz, tetta):
    fig = plt.figure()
    ax = fig.add_subplot(111,  projection='3d')
    ax.plot(xx, yy, zz, zdir='y', linewidth=2.0, color='red')
    ax.plot(xx, zz,  zdir='z', linewidth=1.0, color='grey', linestyle='dashed')
    ax.plot(zz, yy,  zdir='x', linewidth=1.0, color='grey', linestyle='dashed')
    ax.plot(xx, yy,  zdir='y', linewidth=1.0, color='grey', linestyle='dashed')
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.set_zlabel('y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5000))
    plt.show()
    #fig.savefig('res/path_tetta_'+str(tetta)+'.png')

def IntegralPlot(II, yy):
    fig, ax = plt.subplots()
    ax.plot(II, yy, linewidth=2.0, color='red')
    ax.set_xlabel('I')
    ax.set_ylabel('y')

    plt.show()
def windPathPlot(h ,xx, yy, zz):
    fig, axs = plt.subplots(2, 2)

    axs[0, 0].plot(xx, h, linewidth=2.0, color='red')
    axs[0, 0].set_xlabel('xx')  # Add an x-label to the axes.
    axs[0, 0].set_ylabel('h')  # Add a y-label to the axes.

    axs[0, 1].plot(yy, h, linewidth=2.0, color='red')
    axs[0, 1].set_xlabel('yy')  # Add an x-label to the axes.
    axs[0, 1].set_ylabel('h')  # Add a y-label to the axes.

    axs[1, 1].plot(zz, h, linewidth=2.0, color='red')
    axs[1, 1].set_xlabel('zz')  # Add an x-label to the axes.
    axs[1, 1].set_ylabel('h')  # Add a y-label to the axes.

    plt.show()

def flatPlot(xx, yy ):
    fig, ax = plt.subplots()
    ax.plot(xx, yy, linewidth=2.0, color='red')
    ax.set_xlabel('x')
    ax.set_ylabel('y')


    plt.show()
