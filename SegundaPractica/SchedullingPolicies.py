import socket
import heapq
import time

class Packet:
    def __init__(self, data, weight):
        self.data = data
        self.weight = weight
        self.timestamp = time.time()

    # Sobrecarga del operador '<' para comparar paquetes en función de su relación
    # entre la marca de tiempo y el peso. Esto permite que heapq organice los paquetes
    # de manera que los paquetes con menor peso se envíen primero.
    def __lt__(self, other):
        return (self.timestamp * other.weight) < (other.timestamp * self.weight)

# Función que implementa el algoritmo WFQ utilizando una cola de prioridad (heap)
def wfq_scheduler(queue):
    while queue:
        packet = heapq.heappop(queue)
        yield packet

# Función para enviar paquetes a través de un socket UDP
def send_packet(packet, server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(packet.data.encode('utf-8'), (server_ip, server_port))

def main():
    server_ip = '127.0.0.1'
    server_port = 12345

    # Creación de paquetes de ejemplo con diferentes pesos
    packets = [
        Packet("Paquete 1", 1),
        Packet("Paquete 2", 2),
        Packet("Paquete 3", 3),
        Packet("Paquete 4",2),
        Packet("Paquete 5",1),
        Packet("Paquete 6",1),
    ]

    # Inicialización de la cola de prioridad (heap)
    queue = []

    # Encolamiento de los paquetes en la cola de prioridad
    for packet in packets:
        heapq.heappush(queue, packet)

    # Ejecución del algoritmo WFQ y envío de paquetes
    scheduler = wfq_scheduler(queue)

    for packet in scheduler:
        send_packet(packet, server_ip, server_port)
        print(f"Enviado: {packet.data} con peso {packet.weight}")

if __name__ == "__main__":
    main()