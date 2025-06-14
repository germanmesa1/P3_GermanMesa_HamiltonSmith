import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import pydicom

# Commit 1: Creación de clase Paciente con atributos básicos

class Paciente:
    def __init__(self, nombre, edad, id_paciente, imagen_3d):
        self.nombre = nombre
        self.edad = edad
        self.id = id_paciente
        self.imagen_3d = imagen_3d

# Commit 2: Implementación inicial de ImagenMedica y carga DICOM

class ImagenMedica:
    def __init__(self, ruta=None):
        self.ruta = ruta
        self.volumen = None
        self.info = None

# Commit 3: Método cargar_dicom con ordenamiento por SliceLocation
    
    def cargar_dicom(self, ruta):
        archivos = [f for f in os.listdir(ruta) if f.endswith(".dcm")]
        self.imagenes = [pydicom.dcmread(os.path.join(ruta, f)) for f in archivos]
        self.imagenes.sort(key=lambda x: float(x.SliceLocation) if hasattr(x, 'SliceLocation') else 0)
        self.volumen = np.stack([d.pixel_array for d in self.imagenes])
        self.info = self.imagenes[0]
        return self.volumen
        
# Commit 4: Reconstrucción 3D con visualización de cortes
    
    def reconstruir_3d(self):  
        cortes = [
            (self.volumen[self.volumen.shape[0]//2, :, :], 'Transversal'),
            (self.volumen[:, self.volumen.shape[1]//2, :], 'Coronal'),    
            (self.volumen[:, :, self.volumen.shape[2]//2], 'Sagital')    
        ]
        plt.figure(figsize=(15, 5))
        for i, (corte, titulo) in enumerate(cortes, 1):
            plt.subplot(1, 3, i)
            plt.imshow(corte, cmap='gray')
            plt.title(titulo)
            plt.axis('off')
        plt.show()

    

    def trasladar_corte(self, tx=50, ty=50):  
        corte = self.volumen[self.volumen.shape[0]//2]
        rows, cols = corte.shape
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        trasladada = cv2.warpAffine(corte, M, (cols, rows))
        
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.imshow(corte, cmap='gray')
        plt.title('Original')
        plt.axis('off')
        
        plt.subplot(1, 2, 2)
        plt.imshow(trasladada, cmap='gray')
        plt.title(f'Trasladada ({tx},{ty})')
        plt.axis('off')
        plt.show()
        return trasladada

class ImagenSencilla:  
    def __init__(self, ruta=None):
        self.ruta = ruta
        self.imagen = None

    def cargar_imagen(self, ruta):
        self.imagen = cv2.cvtColor(cv2.imread(ruta), cv2.COLOR_BGR2RGB)
        return self.imagen

    def procesar(self, umbral=127, tipo='binario', kernel_size=3):
        gris = cv2.cvtColor(self.imagen, cv2.COLOR_RGB2GRAY)
        _, binaria = cv2.threshold(gris, umbral, 255, {
            'binario': cv2.THRESH_BINARY,
            'binario_inv': cv2.THRESH_BINARY_INV,
            'truncado': cv2.THRESH_TRUNC,
            'tozero': cv2.THRESH_TOZERO
        }.get(tipo, cv2.THRESH_BINARY))
        
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        morf = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)
        
        resultado = cv2.cvtColor(morf, cv2.COLOR_GRAY2RGB)
        cv2.rectangle(resultado, (50, 50), (200, 200), (255,0,0), 2)
        cv2.putText(resultado, f"Umbral: {umbral}", (60, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        
        plt.figure(figsize=(15,5))
        for i, (img, title) in enumerate(zip(
            [self.imagen, binaria, resultado],
            ['Original', 'Binarizada', 'Resultado']
        ), 1):
            plt.subplot(1, 3, i)
            plt.imshow(img)
            plt.title(title)
            plt.axis('off')
        plt.show()
        return resultado
