# Commit 8: Menú principal con opciones a y b

import cv2                                                            
from matplotlib import pyplot as plt
from clases import Paciente, ImagenMedica, ImagenSencilla

#Aca se crean los diccionarios que almacenan los datos globales
pacientes = {}                                                            #Dic objetos paciente
imagenes_medicas = {}                                                    #Dic imagenes medicas DICOM
imagenes_sencillas = {}                                                    #Dic imagenes sencillas JPG/PNG

def menu():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Cargar DICOM")
        print("2. Crear paciente")
        print("3. Cargar JPG/PNG")
        print("4. Trasladar DICOM")
        print("5. Procesar imagen")
        print("6. Salir")
        
        op = input("Opción: ")

     # Commit 9: Implementación de carga DICOM (Opción 1)
        
        if op == '1':
            ruta = input("Ruta DICOM: ")
            clave = input("Clave para guardar: ")
            img = ImagenMedica()
            img.cargar_dicom(ruta)
            img.reconstruir_3d()  # Método con nombre original
            imagenes_medicas[clave] = img

        # Commit 10: Creación de pacientes (Opción 2)
        
        elif op == '2':
            clave = input("Clave DICOM: ")
            if clave not in imagenes_medicas:
                print("¡Clave no existe!")
                continue
                
            img = imagenes_medicas[clave]
            paciente = Paciente(
                nombre=img.info.get('PatientName', 'Anónimo'),
                edad=img.info.get('PatientAge', 'ND'),
                id_paciente=img.info.get('PatientID', 'ND'),
                imagen_3d=img.volumen
            )
            pacientes[paciente.id] = paciente
            print(f"Paciente {paciente.nombre} creado!")
            
        elif op == '3':
            ruta = input("Ruta imagen: ")
            clave = input("Clave para guardar: ")
            img = ImagenSencilla()  # Nombre original
            img.cargar_imagen(ruta)  # Método con nombre original
            imagenes_sencillas[clave] = img
            plt.imshow(img.imagen)
            plt.axis('off')
            plt.show()

  # Commit 12: Guardado de imágenes trasladadas (Opción 4)
        
        elif op == '4':
            clave = input("Clave DICOM: ")
            if clave not in imagenes_medicas:
                print("¡Clave no existe!")
                continue
                
            tx = int(input("Traslación X (default 50): ") or 50)
            ty = int(input("Traslación Y (default 50): ") or 50)
            
            img_trasladada = imagenes_medicas[clave].trasladar_corte(tx, ty)
            nombre_archivo = f"trasladada_{clave}.png"
            cv2.imwrite(nombre_archivo, img_trasladada)     # Commit 13: Guardar imagen
      
            print(f" Imagen trasladada guardada como: {nombre_archivo}")
            
# Commit 11: Procesamiento de JPG/PNG (Opción 5)
        
        elif op == '5':
            clave = input("Clave imagen: ")
            if clave not in imagenes_sencillas:
                print("¡Clave no existe!")
                continue
                
            umbral = int(input("Umbral (0-255): "))
            tipo = input("Tipo (binario/binario_inv/truncado/tozero): ")
            kernel = int(input("Tamaño kernel (impar): "))
            resultado = imagenes_sencillas[clave].procesar(umbral, tipo, kernel)
            nombre_archivo = f"procesada_{clave}.png"
            cv2.imwrite(nombre_archivo, cv2.cvtColor(resultado, cv2.COLOR_RGB2BGR))
            print(f" Imagen procesada guardada como: {nombre_archivo}")
            
        elif op == '6':
            break

if __name__ == "__main__":
    menu()
