import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pickle
import threading

# Ruta del archivo de configuración para almacenar la última ruta seleccionada
CONFIG_FILE = "config.pickle"

def save_config():
    # Guardar la última ruta seleccionada y los argumentos seleccionados en el archivo de configuración
    config = {
        "last_file_path": bat_file_path.get(),
        "config_args": [arg.get() for arg in config_vars],
        "performance_args": [arg.get() for arg in performance_vars],
        "functions_args": [arg.get() for arg in functions_vars]
    }
    with open(CONFIG_FILE, "wb") as file:
        pickle.dump(config, file)

def load_config():
    # Cargar la última ruta seleccionada y los argumentos seleccionados desde el archivo de configuración
    try:
        with open(CONFIG_FILE, "rb") as file:
            config = pickle.load(file)
            last_file_path = config.get("last_file_path", "")
            if last_file_path:
                bat_file_path.set(last_file_path)

            config_args_values = config.get("config_args", [])
            performance_args_values = config.get("performance_args", [])
            functions_args_values = config.get("functions_args", [])

            for var, value in zip(config_vars, config_args_values):
                var.set(value)
            for var, value in zip(performance_vars, performance_args_values):
                var.set(value)
            for var, value in zip(functions_vars, functions_args_values):
                var.set(value)

            # Actualizar los argumentos seleccionados en las pestañas correspondientes
            update_selected_arguments()
    except FileNotFoundError:
        pass

def update_selected_arguments():
    # Actualizar los argumentos seleccionados en las pestañas de Configuración, Rendimiento y Funciones
    selected_config_args = [arg.get() for arg in config_vars]
    selected_performance_args = [arg.get() for arg in performance_vars]
    selected_functions_args = [arg.get() for arg in functions_vars]

    # Marcar los argumentos seleccionados en la pestaña de Configuración
    for var, selected in zip(config_vars, selected_config_args):
        var.set(selected)

    # Marcar los argumentos seleccionados en la pestaña de Rendimiento
    for var, selected in zip(performance_vars, selected_performance_args):
        var.set(selected)

    # Marcar los argumentos seleccionados en la pestaña de Funciones
    for var, selected in zip(functions_vars, selected_functions_args):
        var.set(selected)

def select_bat_file():
    # Abrir el cuadro de diálogo para seleccionar el archivo .bat
    file_path = filedialog.askopenfilename(filetypes=[("Archivo BAT", "*.bat")])

    # Actualizar la variable de ruta del archivo
    bat_file_path.set(file_path)

    # Cargar los argumentos existentes en el archivo seleccionado
    load_existing_arguments(file_path)
    update_selected_arguments()

def load_existing_arguments(file_path):
    # Leer el contenido actual del archivo .bat
    with open(file_path, "r") as file:
        content = file.readlines()

    # Buscar la línea "set COMMANDLINE_ARGS="
    for i, line in enumerate(content):
        if line.startswith("set COMMANDLINE_ARGS="):
            existing_args_line = line
            break
    else:
        # No se encontró la línea, no hay argumentos existentes
        return

    # Obtener los argumentos existentes
    existing_args = existing_args_line.strip().split("=")[1].split()

    # Marcar los argumentos existentes en la pestaña de Configuración
    for arg, var in zip(config_args, config_vars):
        if arg in existing_args:
            var.set(1)
        else:
            var.set(0)

    # Marcar los argumentos existentes en la pestaña de Rendimiento
    for arg, var in zip(performance_args, performance_vars):
        if arg in existing_args:
            var.set(1)
        else:
            var.set(0)

    # Marcar los argumentos existentes en la pestaña de Funciones
    for arg, var in zip(functions_args, functions_vars):
        if arg in existing_args:
            var.set(1)
        else:
            var.set(0)

def update_bat_file():
    # Obtener la ruta del archivo .bat
    file_path = bat_file_path.get()

    # Leer el contenido actual del archivo .bat
    with open(file_path, "r") as file:
        content = file.readlines()

    # Buscar la línea "set COMMANDLINE_ARGS="
    for i, line in enumerate(content):
        if line.startswith("set COMMANDLINE_ARGS="):
            existing_args_line_index = i
            break
    else:
        # No se encontró la línea, agregar una nueva línea al final del archivo
        existing_args_line_index = len(content)

    # Obtener los argumentos seleccionados en la pestaña de Configuración
    selected_config_args = [arg for arg, var in zip(config_args, config_vars) if var.get() == 1]

    # Obtener los argumentos seleccionados en la pestaña de Rendimiento
    selected_performance_args = [arg for arg, var in zip(performance_args, performance_vars) if var.get() == 1]

    # Obtener los argumentos seleccionados en la pestaña de Funciones
    selected_functions_args = [arg for arg, var in zip(functions_args, functions_vars) if var.get() == 1]

    # Generar la línea actualizada "set COMMANDLINE_ARGS="
    new_commandline_args = " ".join(selected_config_args + selected_performance_args + selected_functions_args)
    updated_args_line = f"set COMMANDLINE_ARGS={new_commandline_args}\n"

    # Reemplazar o agregar la línea en el contenido del archivo
    if existing_args_line_index < len(content):
        content[existing_args_line_index] = updated_args_line
    else:
        content.append(updated_args_line)

    # Escribir el contenido actualizado en el archivo .bat
    with open(file_path, "w") as file:
        file.writelines(content)

    # Mostrar un mensaje de éxito
    tk.messagebox.showinfo("Archivo Actualizado", "El archivo .bat ha sido actualizado correctamente.")

def update_interface():
    # Actualizar los elementos de la interfaz gráfica en las pestañas de Configuración, Rendimiento y Funciones aquí

    # Programar la próxima actualización después de un cierto período de tiempo
    window.after(100, update_interface)

# Llamar a la función update_interface para iniciar las actualizaciones
    update_interface()

def execute_bat_file():
    # Obtener la ruta del archivo .bat
    file_path = bat_file_path.get()

    # Definir una función para ejecutar el archivo .bat en un hilo separado
    def run_bat_file():
        import subprocess
        subprocess.call(file_path, shell=True)

    # Crear un hilo para ejecutar el archivo .bat
    t = threading.Thread(target=run_bat_file)
    t.start()

    # Ocultar la ventana principal sin cerrarla
    window.iconify()

    # Cerrar la ventana principal después de un breve retraso
    window.after(1000, window.destroy)

# Crear la ventana principal
window = tk.Tk()
window.title("Automatic1111 Launcher")
window.geometry("400x600")

# Crear el control de pestañas
tab_control = ttk.Notebook(window)

# Crear las pestañas
config_tab = ttk.Frame(tab_control)
performance_tab = ttk.Frame(tab_control)
functions_tab = ttk.Frame(tab_control)

# Agregar las pestañas al control de pestañas
tab_control.add(config_tab, text="Configuración")
tab_control.add(performance_tab, text="Rendimiento")
tab_control.add(functions_tab, text="Funciones")

# Agregar el control de pestañas a la ventana principal
tab_control.pack(expand=1, fill="both")

# Crear el contenedor de desplazamiento para la pestaña de Configuración
config_scroll = ttk.Scrollbar(config_tab)
config_scroll.pack(side="right", fill="y")

# Crear el marco interior para la pestaña de Configuración con desplazamiento
config_inner_canvas = tk.Canvas(config_tab, yscrollcommand=config_scroll.set)
config_inner_frame = ttk.Frame(config_inner_canvas)

# Configurar el marco interior dentro del lienzo
config_inner_canvas.create_window((0, 0), window=config_inner_frame, anchor="nw")
config_inner_frame.bind("<Configure>", lambda event: config_inner_canvas.configure(scrollregion=config_inner_canvas.bbox("all")))

# Configurar la barra de desplazamiento vertical para interactuar con el lienzo
config_scroll.config(command=config_inner_canvas.yview)
config_inner_canvas.config(yscrollcommand=config_scroll.set)

# Empaquetar el lienzo y la barra de desplazamiento en la pestaña de Configuración
config_inner_canvas.pack(side="left", fill="both", expand=True)
config_scroll.pack(side="right", fill="y")

# Crear los controles de casillas de verificación para la pestaña de Configuración
config_args = [
    "--help", "--exit", "--data-dir", "--config", "--ckpt", "--ckpt-dir", "--no-download-sd-model",
    "--vae-dir", "--vae-path", "--gfpgan-dir", "--gfpgan-model", "--codeformer-models-path",
    "--gfpgan-models-path", "--esrgan-models-path", "--bsrgan-models-path", "--realesrgan-models-path",
    "--scunet-models-path", "--swinir-models-path", "--ldsr-models-path", "--lora-dir", "--clip-models-path",
    "--embeddings-dir", "--textual-inversion-templates-dir", "--hypernetwork-dir", "--localizations-dir",
    "--styles-file", "--ui-config-file", "--no-progressbar-hiding", "--max-batch-count", "--ui-settings-file",
    "--allow-code", "--share", "--listen", "--port", "--hide-ui-dir-config", "--disable-console-progressbars", "--enable-console-prompts", "--api", "--api-auth", "--api-log",
    "--nowebui", "--ui-debug-mode", "--device-id", "--administrator", "--cors-allow-origins",
    "--cors-allow-origins-regex", "--tls-keyfile", "--tls-certfile", "--disable-tls-verify", "--server-name",
    "--no-gradio-queue", "--no-hashing", "--skip-version-check", "--skip-python-version-check",
    "--skip-torch-cuda-test", "--skip-install"
]

config_vars = []

for arg in config_args:
    var = tk.IntVar()  # Usar IntVar en lugar de StringVar para obtener valores 0 o 1
    check_button = ttk.Checkbutton(config_inner_frame, text=arg, variable=var)
    check_button.pack(anchor="w")
    config_vars.append(var)

# Crear el contenedor de desplazamiento para la pestaña de Rendimiento
performance_scroll = ttk.Scrollbar(performance_tab)
performance_scroll.pack(side="right", fill="y")

# Crear el marco interior para la pestaña de Rendimiento con desplazamiento
performance_inner_canvas = tk.Canvas(performance_tab, yscrollcommand=performance_scroll.set)
performance_inner_frame = ttk.Frame(performance_inner_canvas)

# Configurar el marco interior dentro del lienzo
performance_inner_canvas.create_window((0, 0), window=performance_inner_frame, anchor="nw")
performance_inner_frame.bind("<Configure>", lambda event: performance_inner_canvas.configure(scrollregion=performance_inner_canvas.bbox("all")))

# Configurar la barra de desplazamiento vertical para interactuar con el lienzo
performance_scroll.config(command=performance_inner_canvas.yview)
performance_inner_canvas.config(yscrollcommand=performance_scroll.set)

# Empaquetar el lienzo y la barra de desplazamiento en la pestaña de Rendimiento
performance_inner_canvas.pack(side="left", fill="both", expand=True)
performance_scroll.pack(side="right", fill="y")

# Crear los controles de casillas de verificación para la pestaña de Rendimiento
performance_args = [
    "--xformers", "--force-enable-xformers", "--xformers-flash-attention", "--opt-sdp-attention",
    "--opt-sdp-no-mem-attention", "--opt-split-attention", "--opt-split-attention-invokeai",
    "--opt-split-attention-v1", "--opt-sub-quad-attention", "--sub-quad-q-chunk-size",
    "--sub-quad-kv-chunk-size", "--sub-quad-chunk-threshold", "--opt-channelslast",
    "--disable-opt-split-attention", "--disable-nan-check", "--use-cpu", "--no-half",
    "--precision", "--no-half-vae", "--upcast-sampling", "--medvram", "--lowvram", "--lowram",
    "--always-batch-cond-uncond"
]

performance_vars = []

for arg in performance_args:
    var = tk.IntVar()
    check_button = ttk.Checkbutton(performance_inner_frame, text=arg, variable=var)
    check_button.pack(anchor="w")
    performance_vars.append(var)

# Crear el contenedor de desplazamiento para la pestaña de Funciones
functions_scroll = ttk.Scrollbar(functions_tab)
functions_scroll.pack(side="right", fill="y")

# Crear el marco interior para la pestaña de Funciones con desplazamiento
functions_inner_canvas = tk.Canvas(functions_tab, yscrollcommand=functions_scroll.set)
functions_inner_frame = ttk.Frame(functions_inner_canvas)

# Configurar el marco interior dentro del lienzo
functions_inner_canvas.create_window((0, 0), window=functions_inner_frame, anchor="nw")
functions_inner_frame.bind("<Configure>", lambda event: functions_inner_canvas.configure(scrollregion=functions_inner_canvas.bbox("all")))

# Configurar la barra de desplazamiento vertical para interactuar con el lienzo
functions_scroll.config(command=functions_inner_canvas.yview)
functions_inner_canvas.config(yscrollcommand=functions_scroll.set)

# Empaquetar el lienzo y la barra de desplazamiento en la pestaña de Funciones
functions_inner_canvas.pack(side="left", fill="both", expand=True)
functions_scroll.pack(side="right", fill="y")

# Crear los controles de casillas de verificación para la pestaña de Funciones
functions_args = [
    "--autolaunch", "--theme", "--use-textbox-seed", "--disable-safe-unpickle", "--ngrok",
    "--ngrok-region", "--update-check", "--update-all-extensions", "--reinstall-xformers",
    "--reinstall-torch", "--tests", "--no-tests"
]

functions_vars = []

for arg in functions_args:
    var = tk.IntVar()
    check_button = ttk.Checkbutton(functions_inner_frame, text=arg, variable=var)
    check_button.pack(anchor="w")
    functions_vars.append(var)

# Crear un frame contenedor
file_frame = ttk.Frame(window)
file_frame.pack(side="top", anchor="nw", pady=5)

# Crear el botón "Seleccionar archivo" para elegir la ruta del archivo .bat
select_file_button = ttk.Button(file_frame, text="Seleccionar archivo", command=select_bat_file)
select_file_button.pack(side="left", padx=4)

# Mostrar la ruta del archivo seleccionado
bat_file_path = tk.StringVar()
selected_file_label = ttk.Label(file_frame, textvariable=bat_file_path)
selected_file_label.pack(side="left")

# Crear el frame para los botones "Actualizar" y "Ejecutar"
button_frame = ttk.Frame(window)
button_frame.pack(side="left", pady=5)

# Crear los botones de Actualizar y Ejecutar
update_button = ttk.Button(button_frame, text="Actualizar", command=update_bat_file)
update_button.pack(side="left", padx=4)

execute_button = ttk.Button(button_frame, text="Ejecutar", command=execute_bat_file)
execute_button.pack(side="left")

# Cargar la última ruta seleccionada al iniciar la aplicación
load_config()

# Ejecutar la aplicación
window.mainloop()

# Guardar la configuración al cerrar la aplicación
save_config()
