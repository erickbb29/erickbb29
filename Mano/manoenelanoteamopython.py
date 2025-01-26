import tkinter as tk
import serial
import speech_recognition as sr
import re  # Para manejar las expresiones regulares

# Configura el puerto serial
ser = serial.Serial('COM3', 9600, timeout=1)

modo_automatico = False
mover_a_180 = False

# Crear la ventana principal
root = tk.Tk()
root.title("Control de Mano")

# Crear etiquetas de estado para el modo automático y el reconocimiento de voz
estado_automatico = tk.Label(root, text="Modo Automático: Desactivado", fg="red", font=("Helvetica", 12))
estado_automatico.pack()

estado_voz = tk.Label(root, text="Reconocimiento de Voz: No iniciado", fg="purple", font=("Helvetica", 12))
estado_voz.pack()

# Crear etiquetas de estado para cada servo
estado_servo_1 = tk.Label(root, text="Indice: 0 grados", fg="blue", font=("Helvetica", 12))
estado_servo_1.pack()

estado_servo_2 = tk.Label(root, text="Medio: 0 grados", fg="blue", font=("Helvetica", 12))
estado_servo_2.pack()

estado_servo_3 = tk.Label(root, text="Anular: 0 grados", fg="blue", font=("Helvetica", 12))
estado_servo_3.pack()

estado_servo_4 = tk.Label(root, text="Menique: 0 grados", fg="blue", font=("Helvetica", 12))
estado_servo_4.pack()

estado_servo_5 = tk.Label(root, text="Pulgar: 0 grados", fg="blue", font=("Helvetica", 12))
estado_servo_5.pack()

# Función para reconocimiento de voz
def reconocer_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        estado_voz.config(text="Reconocimiento de Voz: Escuchando...", fg="orange")
        print("Escuchando...")
        audio = r.listen(source)
        try:
            comando = r.recognize_google(audio, language="es-ES")  # Detecta comandos en español
            print(f"Comando reconocido: {comando}")
            procesar_comando(comando.lower())  # Convierte el comando a minúsculas para facilitar la comparación
            estado_voz.config(text=f"Comando reconocido: {comando}", fg="green")
        except sr.UnknownValueError:
            print("No se entendió el comando")
            estado_voz.config(text="Error: No se entendió el comando", fg="red")
        except sr.RequestError:
            print("Error al conectarse al servicio de reconocimiento de voz")
            estado_voz.config(text="Error al conectarse al reconocimiento de voz", fg="red")

# Procesar el comando de voz
def procesar_comando(comando):
    global mover_a_180, modo_automatico

    if "activar automático" in comando:
        alternar_automatico()
    elif "mover todos" in comando:
        mover_todos_servos()
    else:
        # Detectar si el comando incluye instrucciones para mover servos individuales
        mover_servo_por_comando(comando)

# Mueve un servo específico basado en el comando de voz
def mover_servo_por_comando(comando):
    # Expresión regular para detectar comandos tipo "mover servo 1 a 90 grados"
    patron = r"servo (\d) a (\d+)"
    coincidencia = re.search(patron, comando)
    
    if coincidencia:
        servo_num = int(coincidencia.group(1))  # Obtiene el número del servo
        angulo = int(coincidencia.group(2))  # Obtiene el ángulo deseado

        # Verifica que el ángulo esté entre 0 y 180 grados
        if 0 <= angulo <= 180:
            sliders[servo_num - 1].set(angulo)  # Ajusta el slider correspondiente
            ser.write(f"S{servo_num}:{angulo}\n".encode())  # Envia el comando al puerto serial
            actualizar_etiqueta_servo(servo_num, angulo)
            print(f"Enviado: S{servo_num}:{angulo}")
        else:
            print("Ángulo fuera de rango. Debe estar entre 0 y 180.")
    else:
        print("Comando no reconocido para mover servo.")

# Actualiza la etiqueta del servo correspondiente
def actualizar_etiqueta_servo(servo_num, angulo):
    if servo_num == 1:
        estado_servo_1.config(text=f"Indice: {angulo} grados")
    elif servo_num == 2:
        estado_servo_2.config(text=f"Medio: {angulo} grados")
    elif servo_num == 3:
        estado_servo_3.config(text=f"Anular: {angulo} grados")
    elif servo_num == 4:
        estado_servo_4.config(text=f"Menique: {angulo} grados")
    elif servo_num == 5:
        estado_servo_5.config(text=f"Pulgar: {angulo} grados")

# Actualiza los servos cuando se mueven los sliders
def actualizar_servos(event=None):
    if not modo_automatico:
        angulos = [slider1.get(), slider2.get(), slider3.get(), slider4.get(), slider5.get()]
        for i, angulo in enumerate(angulos):
            ser.write(f"S{i+1}:{angulo}\n".encode())
            actualizar_etiqueta_servo(i + 1, angulo)
            print(f"Enviado: S{i+1}:{angulo}")  # Depuración

# Alterna entre el modo automático y manual
def alternar_automatico():
    global modo_automatico
    modo_automatico = not modo_automatico
    if modo_automatico:
        boton_auto.config(text="Desactivar Automático", bg="red", fg="white")
        ser.write(b'AUTO\n')  # Enviar comando para activar el modo automático
        estado_automatico.config(text="Modo Automático: Activado", fg="green")
        mostrar_posiciones_servos()  # Mostrar posiciones de los servos en la interfaz
    else:
        boton_auto.config(text="Activar Automático", bg="green", fg="white")
        ser.write(b'STOP\n')  # Enviar comando para detener el modo automático
        estado_automatico.config(text="Modo Automático: Desactivado", fg="red")

# Muestra las posiciones actuales de todos los servos
def mostrar_posiciones_servos():
    for i, slider in enumerate(sliders):
        angulo = slider.get()
        actualizar_etiqueta_servo(i + 1, angulo)  # Actualiza las etiquetas de los servos

# Mueve todos los servos al mismo ángulo
def mover_todos_servos():
    global mover_a_180
    mover_a_180 = not mover_a_180
    angulo = 180 if mover_a_180 else 0
    for i, slider in enumerate(sliders):
        slider.set(angulo)
        actualizar_etiqueta_servo(i + 1, angulo)
    ser.write(f"ALL:{angulo}\n".encode())
    print(f"Enviado: ALL:{angulo}")  # Depuración

# Ajustar el tamaño de la ventana para cubrir el 50% de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = int(screen_width * 0.5)
window_height = int(screen_height * 0.5)
root.geometry(f"{window_width}x{window_height}")

# Crear sliders para cada servo
slider1 = tk.Scale(root, from_=0, to=180, orient='vertical', length=200, label="Servo 1")
slider1.pack(side='left', padx=10, pady=10)
slider1.bind("<Motion>", actualizar_servos)  # Actualizar servos al mover el slider

slider2 = tk.Scale(root, from_=0, to=180, orient='vertical', length=200, label="Servo 2")
slider2.pack(side='left', padx=10, pady=10)
slider2.bind("<Motion>", actualizar_servos)  # Actualizar servos al mover el slider

slider3 = tk.Scale(root, from_=0, to=180, orient='vertical', length=200, label="Servo 3")
slider3.pack(side='left', padx=10, pady=10)
slider3.bind("<Motion>", actualizar_servos)  # Actualizar servos al mover el slider

slider4 = tk.Scale(root, from_=0, to=180, orient='vertical', length=200, label="Servo 4")
slider4.pack(side='left', padx=10, pady=10)
slider4.bind("<Motion>", actualizar_servos)  # Actualizar servos al mover el slider

slider5 = tk.Scale(root, from_=0, to=180, orient='vertical', length=200, label="Servo 5")
slider5.pack(side='left', padx=10, pady=10)
slider5.bind("<Motion>", actualizar_servos)  # Actualizar servos al mover el slider

# Lista de sliders
sliders = [slider1, slider2, slider3, slider4, slider5]

# Crear botones con tamaño aumentado
boton_auto = tk.Button(root, text="Activar Automático", command=alternar_automatico, height=2, width=20, font=("Helvetica", 14))
boton_auto.pack(pady=10)

boton_mover_todos = tk.Button(root, text="Mover Todos los Dedos", command=mover_todos_servos, height=2, width=20, font=("Helvetica", 14))
boton_mover_todos.pack(pady=10)

# Botón para activar el reconocimiento de voz
boton_voz = tk.Button(root, text="Reconocer Voz", command=reconocer_voz, height=2, width=20, font=("Helvetica", 14))
boton_voz.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()
