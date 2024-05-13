import psutil
import time


class NetworkMonitor:
    def __init__(self, interval=180):
        self.interval = interval

    def start_monitoring(self):
        while True:
            net_io = psutil.net_io_counters()
            connections = psutil.net_connections(kind='inet')

            print("=== Estatísticas de Rede ===")
            print(f"Bytes enviados: {net_io.bytes_sent}")
            print(f"Bytes recebidos: {net_io.bytes_recv}")
            print(f"Pacotes enviados: {net_io.packets_sent}")
            print(f"Pacotes recebidos: {net_io.packets_recv}")
            print(f"Erros de transmissão: {net_io.errout}")
            print(f"Erros de recebimento: {net_io.errin}")
            print("=== Conexões de Rede ===")
            for conn in connections:
                print(f"PID: {conn.pid}, Local: {conn.laddr}, Remoto: {conn.raddr}, Estado: {conn.status}")
            print("-------------------------")

            time.sleep(self.interval)


if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.start_monitoring()
