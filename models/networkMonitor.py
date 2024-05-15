import psutil
import socket
import time


class NetworkMonitor:
    def __init__(self):
        pass

    def start_monitoring(self):
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
            protocol = self.get_protocol(conn)
            print(f"PID: {conn.pid}, Local: {conn.laddr}, Remoto: {conn.raddr}, Estado: {conn.status}, Protocolo: {protocol}")
        print("-------------------------")

    def get_protocol(self, conn):
        try:
            if conn.laddr and conn.raddr:
                local_ip, local_port = conn.laddr
                remote_ip, remote_port = conn.raddr
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((remote_ip, remote_port))
                    return "TCP"
            elif conn.laddr and not conn.raddr:
                return "TCP"
            else:
                return "UDP"
        except Exception as e:
            return "Desconhecido"


if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.start_monitoring()
