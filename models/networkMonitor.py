import os
import psutil
import socket
import pandas as pd


class NetworkMonitor:
    def __init__(self):
        pass

    def start_monitoring(self):
        net_io = psutil.net_io_counters()
        connections = psutil.net_connections(kind='inet')

        # Lista para armazenar os dados das conexões
        connection_data = []

        for conn in connections:
            protocol = self.get_protocol(conn)
            local_addr = self.format_address(conn.laddr)
            remote_addr = self.format_address(conn.raddr)
            connection_data.append({
                "PID": conn.pid,
                "Local": local_addr,
                "Remoto": remote_addr,
                "Estado": conn.status,
                "Protocolo": protocol
            })

        # Criar DataFrame com os dados das conexões
        df_connections = pd.DataFrame(connection_data)

        # Obter o caminho da pasta "Downloads"
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        # Caminho completo para o arquivo Excel na pasta "Downloads"
        excel_file_path = os.path.join(downloads_folder, 'network_connections.xlsx')

        # Salvar DataFrame em um arquivo Excel na pasta "Downloads"
        df_connections.to_excel(excel_file_path, index=False)

        print(f"Dados das conexões de rede salvos em '{excel_file_path}'")

    def get_protocol(self, conn):
        try:
            if conn.family == socket.AF_INET and conn.type == socket.SOCK_STREAM:
                return "TCP"
            elif conn.family == socket.AF_INET and conn.type == socket.SOCK_DGRAM:
                return "UDP"
            else:
                return "Desconhecido"
        except Exception as e:
            return "Desconhecido"

    def format_address(self, addr):
        if addr:
            ip, port = addr
            return ip
        else:
            return ""


if __name__ == "__main__":
    monitor = NetworkMonitor()
    monitor.start_monitoring()
