#==============================================================================
#Arquivos disponiveis em https://soundcloud.com/bruno-pires-359168091/sets/ee989a_2017s1-exercicio-mixagem
#==============================================================================

import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import scipy.signal as sig

def fft_(x):
    if x.size%2:
        x = x[:-1]

    X = np.fft.fft(x)
    X = X[0:int(X.size/2+1)]
    return X

def ifft_(X):
    inv = X[:-1]
    inv = inv[::-1]
    inv = inv[:-1]
    X = np.concatenate((X,np.conj(inv)))
    x = np.real(np.fft.ifft(X))
    return x

#==============================================================================
#Configurando
#==============================================================================
#inserindo sons
fs, kick = wav.read('audio/myupmix/01_Kick.wav')
fs, snare = wav.read('audio/myupmix/02_SnareUp.wav')
fs, over = wav.read('audio/myupmix/03_Overheads.wav')
fs, cymb = wav.read('audio/myupmix/04_Cymbals.wav')
fs, bass = wav.read('audio/myupmix/05_Bass.wav')
fs, cong = wav.read('audio/myupmix/06_Congas.wav')
fs, guit = wav.read('audio/myupmix/07_ElecGtr1.wav')
fs, guit2 = wav.read('audio/myupmix/08_ElecGtr2.wav')
fs, voic = wav.read('audio/myupmix/10_Vox01.wav')

#ajustando os shapes para 40s
kick = kick[0:1700000]
snare = snare[0:1700000]
over = over[0:1700000,0]
cymb = cymb[0:1700000]
bass = bass[0:1700000]
cong = cong[0:1700000]
guit = guit[0:1700000]
guit2 = guit2[0:1700000]
voic = voic[0:1700000]

kick.shape = ( (kick.shape[0]), 1)
snare.shape = ( (snare.shape[0]), 1)
over.shape = ( (over.shape[0]), 1)
cymb.shape = ( (cymb.shape[0]), 1)
bass.shape = ( (bass.shape[0]), 1)
cong.shape = ( (cong.shape[0]), 1)
guit.shape = ( (guit.shape[0]), 1)
guit2.shape = ( (guit2.shape[0]), 1)
voic.shape = ( (voic.shape[0]), 1)

#==============================================================================
#Efeitos
#==============================================================================

#Distorcao (clip) em ambas guitarras, mais suave na guit2
guit = np.minimum(0.8, guit * 0.001)
guit = np.maximum((0.8*-1), guit)

guit2 = np.minimum(0.8, guit2 * 0.002)
guit2 = np.maximum((0.8*-1), guit2)

#Filtro passa baixas para manter apenas o timbre mais grave do baixo
BASS = fft_(bass)
win = np.zeros(BASS.size)
W0 = 0
W1 = int(1/(fs/4)*BASS.size)
win[W0:W1] = 1
BASS_win = np.multiply(BASS,win)
bass = ifft_(DUET_win)
bass = np.asarray(bass, dtype=np.int16)

#==============================================================================
#mixagem estereo
#==============================================================================
matriz_estereo = np.hstack( (kick, snare, over, cymb, bass, cong, guit, voic, guit2) )

#configurando volumes para mixagem estereo (bateria completa a esquerda, outros a direita, voz em ambos canais)
mixleft = np.array( [[0.0005],[0.0005],[0.0005],[0.0005],[0],[0],[0],[0.0002],[0]])
mixright = np.array( [[0],[0],[0],[0],[0.001],[0.0001],[0.1],[0.0002],[0.1]])
mixagem_estereo = np.hstack((mixleft,mixright))

#salvando som mixado estereo
mixado_estereo = np.dot(matriz_estereo, mixagem_estereo)

#==============================================================================
#Adicionando reverberacao do madson square garden
#==============================================================================
fs, conv = wave.read('audio/myupmix/msg.wav')

mixado_estereo = np.convolve(conv, mixado_estereo)
mixado_estereo = 0.8 * mixado_estereo / np.max(mixado_estereo)

#==============================================================================
#Salvando a versao final do arquivo
#==============================================================================
wav.write('TrabalhoFinal40s.wav', fs, mixado_estereo)


#Grafico
#plt.figure()
#plt.plot(voic)
#plt.show()
