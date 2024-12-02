import re
import matplotlib.pyplot as plt
import argparse

# Configurar o argparse para receber argumentos de linha de comando
parser = argparse.ArgumentParser(description="Gerar gráficos de Request Duration e Average Latency a partir de um arquivo .log")
parser.add_argument("log_file", help="Caminho para o arquivo .log")
parser.add_argument("-o", "--output", default="request_duration_graph.png", help="Caminho para salvar o gráfico (opcional)")
args = parser.parse_args()

# Listas para armazenar os valores extraídos
request_durations = []
selected_servers = []

# Regex para capturar os valores de Request Duration e Selected Server
request_duration_regex = r"Request duration: ([\d\.]+) ms"
selected_server_regex = r"Selected server: (.+)"

# Ler o arquivo e extrair os dados
try:
    with open(args.log_file, "r") as file:
        for line in file:
            duration_match = re.search(request_duration_regex, line)
            server_match = re.search(selected_server_regex, line)
            if duration_match:
                request_durations.append(float(duration_match.group(1)))
            if server_match:
                selected_servers.append(server_match.group(1))
except FileNotFoundError:
    print(f"Erro: Arquivo '{args.log_file}' não encontrado.")
    exit(1)

# Verificar se há dados para plotar
if not request_durations or not selected_servers:
    print("Nenhum dado válido encontrado no arquivo.")
    exit(1)

# Mapear cores para cada servidor
unique_servers = list(set(selected_servers))
unique_servers.sort()
colors = {server: plt.cm.tab10(i) for i, server in enumerate(unique_servers)}

# Gerar o gráfico
plt.figure(figsize=(12, 6))
for i, duration in enumerate(request_durations):
    plt.bar(i, duration, color=colors[selected_servers[i]])

# Adicionar rótulos e legenda
plt.title("Request Duration by Selected Server")
plt.xlabel("Request Index")
plt.ylabel("Request Duration (ms)")
plt.xticks(range(len(request_durations)), range(1, len(request_durations) + 1))
plt.legend([plt.Rectangle((0, 0), 1, 1, color=colors[server]) for server in unique_servers], unique_servers, title="Selected Server")
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Salvar o gráfico como imagem
output_image_path = args.output
plt.savefig(output_image_path)
plt.close()

print(f"Gráfico salvo em: {output_image_path}")
