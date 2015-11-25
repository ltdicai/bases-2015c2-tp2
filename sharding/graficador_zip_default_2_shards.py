#! usr/bin/python
from matplotlib.pyplot import *
from numpy import *
from pylab import *

def graficar_1():
  total_documentos = [20000,40000,60000,80000,100000,
                      120000, 140000, 160000, 180000, 200000,
                      220000, 240000, 260000, 280000, 300000,
                      320000, 340000, 360000, 380000, 400000,
                      420000, 440000, 460000, 480000, 500000
                      ]

  shard_0 = [18206, 36420, 54571, 72757, 90974,
             109137, 127278, 107600, 121062, 134519,
             147965, 161489, 174891, 188442, 201820,
             215297, 228746, 242237, 255727, 269198,
             282586, 296029, 309452, 322835, 336335
            ]

  shard_1 = [1794, 3580, 5429, 7243, 9026,
             10863, 12722, 52400, 58938, 65481,
             72035, 78511, 85109, 91558, 98180,
             104703, 111254, 117763, 124273, 130802,
             137414, 143971, 150548, 157165, 163665
            ]

  #Dominio para e
  #t = np.linspace(0.,40., 1024, endpoint = True)

  #Plot generico
  plot(total_documentos,shard_0, color="blue", linewidth = 1.0, linestyle="-", label= "Shard 0")
  plot(total_documentos,shard_1, color="red", linewidth = 1.0 , linestyle = "-", label = "Shard 1")

  legend(loc='upper right')

  xlabel('Cant total de documentos')
  ylabel('Cant documentos por shard')


  savefig("./exp1.jpg")
  close()

graficar_1()
