#importation des librairies
import matplotlib.pyplot as pyplot
import numpy as np
import math 
import time

# Record the start time
start_time = time.time()

#Lire l’image
image = pyplot.imread("pns_original.png")

#Tronquer l’image à des multiples de 8 en x et y
x = image.shape[0] - image.shape[0]%8
y = image.shape[1] - image.shape[1]%8

#On initialise la matrice finale 
final = np.zeros((x,y,3))

#On initialise le taux et l'erreur de compression
taux = 0
erreur = 0

#On défini la matrice de passage en fréquentiel de la DCT-2 P
P = np.zeros((8,8))
P[0,:] = 1/math.sqrt(8)
for i in range(1,8):
    for j in range(0,8):
        P[i,j] = math.cos((2*j+1)*i*math.pi/16)/2

#verification que P*PT=Id
np.matmul(P,np.transpose(P))

# matrice de quantification de la norme JPEG
Q = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 13, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
    ])
    
Q_highquality = np.array([
    [2,  1,  1,  2,  2,  4,  5,  4 ],
    [ 1,  1,  2,  3,  2,  6,  6,  6 ],
    [ 2,  2,  2,  2,  4,  9,  8 , 7 ],
    [ 2,  2,  2,  2,  5,  8,  9,  7 ],
    [ 2,  2,  4,  5,  7,  12, 11, 9 ],
    [ 3,  4,  7,  9,  11, 11, 10,  8 ],
    [ 5,  7,  8,  9,  10, 12, 12,  10 ],
    [ 7,  8,  9,  10, 11, 10, 10,  10 ],
])

Q_lowquality = np.array([
    [64, 55, 50, 64, 96, 160, 204, 244],
    [55, 56, 66, 80, 111, 156, 160, 140],
    [66, 65, 80, 120, 160, 228, 280, 224],
    [75, 82, 110, 145, 204, 348, 320, 248],
    [92, 112, 160, 192, 224, 364, 344, 260],
    [120, 175, 220, 248, 300, 384, 404, 332],
    [260, 320, 400, 420, 440, 484, 480, 404],
    [392, 520, 520, 520, 560, 500, 520, 520]
])

#On boucle sur les trois couleurs
for h in range(np.minimum(image.shape[2],3)):
               
    # On transfome les intensités entre 0 et 1 en entiers entre 0 et 255, puis on centre pour se ramener entre −128 et 127
    couleur = image[0:x,0:y,h]
    couleur = (couleur*255).astype(int)-128

    #Compression, Comp = matrice compressée
    Comp = np.zeros_like(couleur)
    
    #Création de matrice 8x8 avec i+j comme valeur à chaque indice i+j
    indice = (np.arange(8)[:, None] + np.arange(8))
    
    for i in range(0,int(x/8)):
        
        for j in range(0,int(y/8)):

            #Pour chaque bloc 8 × 8 de l’image :
            Bloc8 = couleur[i*8:i*8+8,j*8:j*8+8]
            #Appliquer le changement de base D = PMP T
            D = np.matmul(P,np.matmul(Bloc8,(np.transpose(P))))

            D = np.divide(D, Q).astype(int)
            #On met à 0 tous les coefficients D qui vérifient i+j > 2
            D[indice > 6]=0
            # Appliquer la matrice de quantification terme à terme D./Q et prendre la partie entière
            Comp[i * 8:i * 8 + 8, j * 8:j * 8 + 8] = D
                  
    #Calcul du taux de compression pour chaque couleur
    taux += 1-(np.count_nonzero(Comp))/(x*y)
    
    #Decompression, Décomp = matrice décompressée
    Decomp = np.zeros_like(couleur)
    
    for i in range(int(x/8)):
        for j in range(int(y/8)):
            #Pour chaque bloc 8 × 8 :
            Bloc8 = Comp[i*8:i*8+8, j*8:j*8+8]
            #Multiplier par la matrice Q terme à terme
            X = np.multiply(Bloc8,Q).astype(int)
            #Appliquer la transformée inverse PTDP
            Decomp[i*8:i*8+8,j*8:j*8+8] = np.matmul((np.transpose(P)),np.matmul(X,P))
            
    #Comparer cette matrice avec la matrice originale (en norme L2 relative)
    erreurAbsolue = np.linalg.norm(Decomp-couleur)
    erreurTheorique = np.linalg.norm(couleur)

    #Calcul de l'erreur de compression pour chaque couleur
    erreur += np.sqrt((erreurAbsolue*erreurAbsolue)/(erreurTheorique*erreurTheorique))
    
    #Re-transformer les valeurs entre −128 et 127 en réels entre 0 et 1

    # probleme de maximum 
    # print(final.max())

    # Remplace les valeurs supérieures à 255 par 255
    # Remplace les valeurs inférieures à 0 par 0
    # On transfome les intensités entre 0 et 1
    final[:, :, h] = np.clip(Decomp + 128, 0, 255) / 255


#taux de compression et erreur de compression totale
print("le taux de compression est ", taux/3)
print("l'erreur de compression est", erreur/3)

#sauver l’image (pour la comparer visuellement)
pyplot.imsave("final.png",final)
    
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time in seconds
print(f"Execution time: {elapsed_time} seconds")

pyplot.imshow(final)
pyplot.axis ("off")
pyplot.show()