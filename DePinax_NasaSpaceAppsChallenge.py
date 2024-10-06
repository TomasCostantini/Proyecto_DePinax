# Librerias necesarias para la lectura de datos
import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from scipy import signal
from matplotlib import cm
# Función para mostrar el valor seleccionado
cat_directory = './data/lunar/training/catalogs/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'
cat = pd.read_csv(cat_file)
cat_Mars_dir = './data/mars/training/catalogs/'
cat_Mars_file = cat_Mars_dir + 'Mars_InSight_training_catalog_final.csv'
cat_Mars = pd.read_csv(cat_Mars_file)
row = cat.iloc[0]
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
arrival_time
test_filename = row.filename
test_filename

data_directory = './data/lunar/training/data/S12_GradeA/'
mseed_file = f'{data_directory}{test_filename}.mseed'
st = read(mseed_file)
st
# Set the minimum frequency
minfreq = 0.5
maxfreq = 1.0

# This is how you get the data and the time, which is in seconds
tr = st.traces[0].copy()
tr_times = tr.times()
tr_data = tr.data

# Start time of trace (another way to get the relative arrival time using datetime)
starttime = tr.stats.starttime.datetime
arrival = (arrival_time - starttime).total_seconds()
arrival

# Going to create a separate trace for the filter data
st_filt = st.copy()
st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
tr_filt = st_filt.traces[0].copy()
tr_times_filt = tr_filt.times()
tr_data_filt = tr_filt.data

f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

figura = plt.figure(figsize=(10, 10))
eje = plt.subplot(2, 1, 1)
# Plot trace
eje.plot(tr_times_filt,tr_data_filt, color= 'red')

# Mark detection
eje.axvline(x = arrival, color='white',label='Detection')
eje.legend(loc='upper left')
figura.patch.set_facecolor('#515a5a')  # Cambiar el fondo de la figura
plt.xlabel('Time(sec)')
plt.ylabel('Velocity(m/s)')
# Cambiar el color de fondo de los ejes
eje.set_facecolor('#17202a')  # Cambiar el fondo de los ejes
# Make the plot pretty
eje.set_xlim([min(tr_times_filt),max(tr_times_filt)])
eje.set_ylabel('Velocity (m/s)')
eje.set_xlabel('Time (s)')

eje2 = plt.subplot(2, 1, 2)
vals = eje2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=5e-17)
eje2.set_xlim([min(tr_times_filt),max(tr_times_filt)])
#eje2.set_xlabel(f'Tiempo (Fecha Hora:Minuto)', fontweight='bold')
eje2.set_ylabel('Frequency (Hz)', fontweight='bold')
eje2.axvline(x=arrival, c='red')
cbar = plt.colorbar(vals, orientation='horizontal')
cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')



def mostrar_seleccion(event):
    seleccion = combo.get()
    if 'Moon' in seleccion:
        a = fechas_final.index(seleccion)
        row = cat.iloc[a]
        minfreq = 0.5
        maxfreq = 1.0
    if 'Mars' in seleccion:
        a = fechas_final.index(seleccion) - 76
        row = cat_Mars.iloc[a]
        minfreq = 0.5
        maxfreq = 10.0
    
    arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
    arrival_time
    test_filename = row.filename
    test_filename
    if 'Moon' in seleccion:
        data_directory = './data/lunar/training/data/S12_GradeA/'
        mseed_file = f'{data_directory}{test_filename}.mseed'
        fr = 5e-17
        figura.clear()
    if'Mars'in seleccion:
        data_directory = './data/mars/training/data/'
        mseed_file = f'{data_directory}{test_filename}.mseed'
        fr = 10000
        figura.clear()
        
    st = read(mseed_file)
    st
    # Set the minimum frequency
    

    # This is how you get the data and the time, which is in seconds
    tr = st.traces[0].copy()
    tr_times = tr.times()
    tr_data = tr.data

    # Start time of trace (another way to get the relative arrival time using datetime)
    starttime = tr.stats.starttime.datetime
    arrival = (arrival_time - starttime).total_seconds()
    arrival
    # Going to create a separate trace for the filter data
    st_filt = st.copy()
    st_filt.filter('bandpass',freqmin=minfreq,freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data

    f, t, sxx = signal.spectrogram(tr_data_filt, tr_filt.stats.sampling_rate)

    eje = plt.subplot(2, 1, 1)
    # Plot trace
    eje.plot(tr_times_filt,tr_data_filt, color= 'red')
    
    # Mark detection
    eje.axvline(x = arrival, color='white',label='Detection')
    eje.legend(loc='upper left')
    figura.patch.set_facecolor('#515a5a')  # Cambiar el fondo de la figura
    plt.xlabel('Time(sec)')
    plt.ylabel('Velocity(m/s)')
    # Cambiar el color de fondo de los ejes
    eje.set_facecolor('#17202a')  # Cambiar el fondo de los ejes
    # Make the plot pretty
    eje.set_xlim([min(tr_times_filt),max(tr_times_filt)])
    eje.set_ylabel('Velocity (m/s)')
    eje.set_xlabel('Time (s)')
    
    eje2 = plt.subplot(2, 1, 2)
    eje2.clear()
    vals = eje2.pcolormesh(t, f, sxx, cmap=cm.jet, vmax=fr)
    eje2.set_xlim([min(tr_times_filt),max(tr_times_filt)])
    #eje2.set_xlabel(f'Time (Day Hour:Minute)', fontweight='bold')
    #eje2.set_ylabel('Frequency (Hz)', fontweight='bold')
    eje2.axvline(x=arrival, c='red')
    cbar = plt.colorbar(vals, orientation='horizontal')
    #cbar.set_label('Power ((m/s)^2/sqrt(Hz))', fontweight='bold')
    canvas.draw()

# Crear la ventana principal
root = tk.Tk()
root.title("Historic data")

# Crear la barra desplegable (ComboBox)
c = cat['time_abs(%Y-%m-%dT%H:%M:%S.%f)']
d = cat_Mars['time_abs(%Y-%m-%dT%H:%M:%S.%f)']
opciones_Mars = d.tolist()
opciones = c.tolist()
fechas_convertidas = [f'Moon {datetime.strptime(opciones, "%Y-%m-%dT%H:%M:%S.%f")}'for opciones in c]
fechas_mars = [f'Mars {datetime.strptime(opciones_Mars, "%Y-%m-%dT%H:%M:%S.%f")}'for opciones_Mars in d]
suma_fechas = fechas_convertidas + fechas_mars
fechas_final = list(map(str,suma_fechas))
print(fechas_final)  
combo = ttk.Combobox(root, values= fechas_final) 

# Establecer un valor por defecto
combo.current(0)
# Asociar un evento cuando se seleccione una opción
combo.bind("<<ComboboxSelected>>", mostrar_seleccion)
# Colocar el menú desplegable en la ventana
combo.pack(pady=10)
canvas = FigureCanvasTkAgg(figura, master=root)  # Crear un canvas para el gráfico
canvas.draw()  # Dibujar el gráfico
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # Colocar el gráfico en la ventana
root.configure(bg='#515a5a')  # Color de fondo de la ventana
# Iniciar el bucle principal de la interfaz
root.mainloop()