import re
import matplotlib.pyplot as plt
import argparse

# Configurar o argparse para receber argumentos de linha de comando
parser = argparse.ArgumentParser(description="Gerar gráfico de Average Latency a partir de um arquivo .log")
parser.add_argument("log_file", help="Caminho para o arquivo .log")
parser.add_argument("-o", "--output", default="average_latency_graph.png", help="Caminho para salvar o gráfico (opcional)")
args = parser.parse_args()

# Caminho do arquivo
log_file_path = args.log_file

# Lista para armazenar os valores extraídos
average_latencies = []

# Regex para capturar "Average latency: valor ms"
regex = r"Average latency: ([\d\.]+) ms"

# Abrir e ler o arquivo
try:
    with open(log_file_path, "r") as file:
        for line in file:
            match = re.search(regex, line)
            if match:
                average_latencies.append(float(match.group(1)))
except FileNotFoundError:
    print(f"Erro: Arquivo '{log_file_path}' não encontrado.")
    exit(1)

# Verificar se há dados para plotar
if not average_latencies:
    print("Nenhum valor de 'Average latency' encontrado no arquivo.")
    exit(1)

# Gerar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(average_latencies, marker="o", linestyle="-", label="Average Latency")
plt.title("Average Latency Over Time")
plt.xlabel("Request Index")
plt.ylabel("Average Latency (ms)")
plt.legend()
plt.grid(True)

# Salvar o gráfico como imagem
output_image_path = args.output
plt.savefig(output_image_path)
plt.close()

print(f"Gráfico salvo em: {output_image_path}")