import tkinter as tk
from tkinter import messagebox
import requests

import requests

def realizar_prediccion():
    try:
        # 1. SEGURIDAD: URL oficial completa de BigML
        url_base = "https://bigml.io/andromeda/prediction" 
        
        usuario = "tobarsanchezk"
        api_key = "pon la clave de la api aqui" 
        
        url_autenticada = f"{url_base}?username={usuario};api_key={api_key}"

        # 2. DATOS
        payload = {
            "model": "model/6ab83a7b8e747759507ef3ef", 
            "input_data": {
                "000000": int(entrada_embarazos.get()),
                "000001": float(entrada_glucosa.get()),
                "000002": float(entrada_presion.get()),
                "000003": float(entrada_piel.get()),
                "000004": float(entrada_insulina.get()),
                "000005": float(entrada_imc.get()),
                "000006": float(entrada_pedigree.get()),
                "000007": int(entrada_edad.get())
            }
        }

        headers = {
            "Content-Type": "application/json"
        }

        etiqueta_resultado.config(text="Consultando al modelo en la nube...", fg="blue")
        ventana.update() 

        # 3. CONSUMO
        respuesta = requests.post(url_autenticada, json=payload, headers=headers, timeout=15)
        respuesta.raise_for_status() 
        
        # 4. RESULTADO: Imprimimos el texto ABSOLUTO y completo que envía la IA
        print("\n=== RESPUESTA COMPLETA DE BIGML ===")
        print(respuesta.text)
        print("===================================\n")
        
        datos_json = respuesta.json()
        
        # Estrategia de búsqueda profunda: Si está en 'object', lo saca; si no, lo busca en la raíz.
        if "object" in datos_json:
            resultado_final = datos_json["object"].get("output", "Error")
        else:
            resultado_final = datos_json.get("output", datos_json.get("prediction", {}).get("000008", "Error"))
            
        print(f"Diagnóstico puro extraído: {resultado_final}")
        
        # Validamos si la respuesta es el número 1 o la palabra "true"
        if str(resultado_final) == "1" or str(resultado_final).lower() == "true":
            texto_resultado = "Positivo (Riesgo Alto)"
            # Lo pintamos de ROJO para diferenciarlo claramente
            etiqueta_resultado.config(text=f"Diagnóstico de la IA: {texto_resultado}", fg="red")
        else:
            texto_resultado = "Negativo (Riesgo Bajo)"
            etiqueta_resultado.config(text=f"Diagnóstico de la IA: {texto_resultado}", fg="green")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa únicamente números en los campos.")
        etiqueta_resultado.config(text="Esperando datos correctos...", fg="black")
    except requests.exceptions.RequestException as error_red:
        messagebox.showerror("Error", "No se pudo conectar con la API revisa la consola.")
        etiqueta_resultado.config(text="Error de conexión.", fg="red")

# ==========================================
# CONFIGURACIÓN DE LA INTERFAZ GRÁFICA (UI)
# ==========================================
# Instanciar la ventana principal
ventana = tk.Tk()
ventana.title("Predictor de Diabetes - Machine Learning")
ventana.geometry("380x480") # Ancho x Alto
ventana.config(padx=20, pady=20) # Márgenes internos

# Lista estructurada para generar los campos dinámicamente y evitar código muerto/repetido
# Formato: (Texto de la etiqueta, Valor numérico de ejemplo)
campos = [
    ("Embarazos (Cant):", "2"),
    ("Glucosa (mg/dL):", "120"),
    ("Presión Arterial (mm Hg):", "70"),
    ("Grosor de Piel (mm):", "20"),
    ("Insulina (mu U/ml):", "80"),
    ("IMC (Peso/Altura^2):", "25.0"),
    ("Función Pedigree:", "0.45"),
    ("Edad (Años):", "33")
]

entradas = [] # Aquí guardaremos los objetos de entrada (inputs)

# Bucle para dibujar las etiquetas y los campos de texto ordenadamente
for fila, (texto_etiqueta, valor_ejemplo) in enumerate(campos):
    # Crear etiqueta (Label)
    etiqueta = tk.Label(ventana, text=texto_etiqueta, font=("Segoe UI", 10))
    etiqueta.grid(row=fila, column=0, sticky="w", pady=5) # sticky="w" alinea a la izquierda
    
    # Crear campo de entrada (Entry)
    entrada = tk.Entry(ventana, width=15, font=("Segoe UI", 10))
    entrada.insert(0, valor_ejemplo) # Añadir el valor de ejemplo por defecto
    entrada.grid(row=fila, column=1, pady=5)
    entradas.append(entrada)

# Asignar las entradas a variables específicas usando desempaquetado de listas
entrada_embarazos, entrada_glucosa, entrada_presion, entrada_piel, entrada_insulina, entrada_imc, entrada_pedigree, entrada_edad = entradas

# Botón de acción
# bg y fg controlan los colores de fondo y texto (simulando un poco el estilo de botones web)
boton_calcular = tk.Button(ventana, text="Calcular Probabilidad", command=realizar_prediccion, 
                           bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"), cursor="hand2")
boton_calcular.grid(row=len(campos), column=0, columnspan=2, pady=20)

# Etiqueta para mostrar el resultado final
etiqueta_resultado = tk.Label(ventana, text="Esperando datos...", font=("Segoe UI", 11, "bold"))
etiqueta_resultado.grid(row=len(campos)+1, column=0, columnspan=2)

# Iniciar el bucle principal que mantiene la ventana abierta
ventana.mainloop()