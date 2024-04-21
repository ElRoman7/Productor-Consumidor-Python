import threading
import time
import queue
import tkinter as tk

# Constantes para el tamaño del búfer y los tiempos de espera del productor y consumidor
BUFFER_SIZE = 5
PRODUCER_SLEEP = 2
CONSUMER_SLEEP = 3

class ProducerConsumerApp:
    def __init__(self, master):
        # Inicialización de la aplicación y la interfaz gráfica
        self.master = master
        self.master.title("Productor-Consumidor con Semáforos")
        self.master.geometry("400x400")

        # Creación de elementos de la interfaz gráfica
        self.buffer_label = tk.Label(master, text="Buffer:")
        self.buffer_label.pack()

        self.buffer_text = tk.Text(master, height=10, width=50)
        self.buffer_text.pack()

        self.status_label = tk.Label(master, text="")
        self.status_label.pack()

        self.buffer_full_frame = tk.Frame(master, width=20, height=20, bg="green")
        self.buffer_full_frame.pack()

        self.start_button = tk.Button(master, text="Iniciar", command=self.start_threads)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Detener", command=self.stop_threads, state=tk.DISABLED)
        self.stop_button.pack()

        # Creación del búfer y semáforos
        self.buffer = queue.Queue(BUFFER_SIZE)
        self.producer_semaphore = threading.Semaphore(BUFFER_SIZE)  # Semáforo para controlar la producción
        self.consumer_semaphore = threading.Semaphore(0)             # Semáforo para controlar el consumo

        # Inicialización de variables para hilos y estado de la aplicación
        self.producer_thread = None
        self.consumer_thread = None
        self.running = False

    def start_threads(self):
        # Método para iniciar los hilos del productor y consumidor
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Creación y inicio de los hilos
        self.producer_thread = threading.Thread(target=self.producer)
        self.consumer_thread = threading.Thread(target=self.consumer)

        self.producer_thread.start()
        self.consumer_thread.start()

        # Actualización de la GUI
        self.update_gui()

    def stop_threads(self):
        # Método para detener los hilos
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_gui(self):
        # Método para actualizar la interfaz gráfica
        if not self.running:
            return

        self.update_buffer_display()

        self.master.after(1000, self.update_gui)  # Programar próxima actualización en 1 segundo

    def producer(self):
        # Método del productor
        while self.running:
            item = f"Prod_{time.strftime('%H:%M:%S')}"  # Crear un elemento único
            self.producer_semaphore.acquire()            # Adquirir el semáforo de producción
            self.buffer.put(item)                        # Colocar el elemento en el búfer
            self.consumer_semaphore.release()            # Liberar el semáforo de consumo
            time.sleep(PRODUCER_SLEEP)                   # Esperar antes de producir el siguiente elemento

    def consumer(self):
        # Método del consumidor
        while self.running:
            self.consumer_semaphore.acquire()            # Adquirir el semáforo de consumo
            item = self.buffer.get()                     # Obtener un elemento del búfer
            self.producer_semaphore.release()            # Liberar el semáforo de producción
            time.sleep(CONSUMER_SLEEP)                   # Simular procesamiento del elemento

    def update_buffer_display(self):
        # Método para actualizar la visualización del búfer en la GUI
        self.buffer_text.config(state=tk.NORMAL)
        self.buffer_text.delete(1.0, tk.END)
        for item in list(self.buffer.queue):
            self.buffer_text.insert(tk.END, f"{item}\n")
        self.buffer_text.config(state=tk.DISABLED)

        if self.buffer.full():
            self.status_label.config(text="Buffer lleno")
            self.buffer_full_frame.config(bg="red")
        elif self.buffer.empty():
            self.status_label.config(text="Buffer vacío")
            self.buffer_full_frame.config(bg="green")
        else:
            self.status_label.config(text="")

def main():
    # Función principal para iniciar la aplicación
    root = tk.Tk()
    app = ProducerConsumerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
