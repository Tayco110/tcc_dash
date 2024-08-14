import serial
import time

# Configuração da conexão serial
def open_serial_connection(port='COM3', baudrate=9600):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.flushInput()
    return ser

# Função para ler dados da ESP32
def read_sensor_data(ser):
    if ser.in_waiting > 0:
        try:
            line = ser.readline().decode('utf-8').rstrip()
            k, na, cl = map(float, line.split(','))
            return {'K': k, 'Na': na, 'Cl': cl}
        except ValueError:
            print("Erro na leitura dos dados.")
            return None
    return None