# Compression d'images par DCT (JPEG-like)

Implémentation from scratch de la compression d'images par 
Transformée en Cosinus Discrète (DCT), inspirée de la norme JPEG.  
Projet réalisé dans le cadre du cours MAM3 à Polytech Nice-Sophia.

## Description

L'algorithme compresse une image en appliquant sur chaque bloc 8×8 :
1. Un changement de base fréquentiel (DCT-2) : `D = P·M·Pᵀ`
2. Une quantification terme à terme par la matrice JPEG standard
3. Une troncature des hautes fréquences (coefficients i+j > seuil)

La décompression applique les opérations inverses et calcule le taux 
et l'erreur de compression (norme L2 relative).

## Résultats

- Taux de compression : ~85–90%
- Erreur relative : ~10%
- Visuellement indiscernable de l'image originale

## Lancement

```bash
python projet.py
```

L'image `pns_original.png` doit être dans le même répertoire.  
L'image compressée est sauvegardée sous `final.png`.

## Technologies

- Python 3
- NumPy
- Matplotlib

## Structure

- `projet.py` — implémentation principale (quantification JPEG + troncature)
- `test.py` — variante avec seuil de troncature plus agressif
- `pns_original.png` — image de test (Polytech Nice-Sophia)
