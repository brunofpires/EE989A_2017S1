#Arquivos disponíveis em https://soundcloud.com/bruno-pires-359168091/sets/ee989a_2017s1-exercicio-mixagem

import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

#inserindo sons
fs, kick = wav.read('audio/myupmix/01_Kick.wav')
fs, snare = wav.read('audio/myupmix/02_SnareUp.wav')
fs, over = wav.read('audio/myupmix/03_Overheads.wav')
fs, cymb = wav.read('audio/myupmix/04_Cymbals.wav')
fs, bass = wav.read('audio/myupmix/05_Bass.wav')
fs, cong = wav.read('audio/myupmix/06_Congas.wav')
fs, guit = wav.read('audio/myupmix/07_ElecGtr1.wav')
fs, voic = wav.read('audio/myupmix/10_Vox01.wav')

#ajustando os shapes
over = over[0:12220796,0]

kick.shape = ( (kick.shape[0]), 1)
snare.shape = ( (snare.shape[0]), 1)
over.shape = ( (over.shape[0]), 1)
cymb.shape = ( (cymb.shape[0]), 1)
bass.shape = ( (bass.shape[0]), 1)
cong.shape = ( (cong.shape[0]), 1)
guit.shape = ( (guit.shape[0]), 1)
voic.shape = ( (voic.shape[0]), 1)
#==============================================================================
#estereo
#==============================================================================
matriz_estereo = np.hstack( (kick, snare, over, cymb, bass, cong, guit, voic) )

#configurando volumes para mixagem estereo (bateria esquerda, outros a direita)
mix1 = np.array( [[0.00001],[0.0001],[0.0001],[0.0001],[0],[0],[0],[0]])
mix2 = np.array( [[0],[0],[0],[0],[0.0001],[0.0001],[0.0001],[0.0001]])
mixagem_estereo = np.hstack((mix1,mix2))

#salvando som mixado estereo
mixado_estereo = np.dot(matriz_estereo, mixagem_estereo)
wav.write('3_mixado_estereo.wav', fs, mixado_estereo)

#vendo espectro
#plt.figure()
#plt.plot(mixado)
#plt.show()
