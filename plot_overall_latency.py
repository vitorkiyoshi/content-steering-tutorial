import re
import matplotlib.pyplot as plt
import argparse
import numpy as np

# Configurar o argparse para receber argumentos de linha de comando
parser = argparse.ArgumentParser(description="Gerar gráfico com média, máximo e mínimo das latências a partir de múltiplos arquivos .log")
parser.add_argument("log_files", nargs='+', help="Caminhos para os arquivos .log")
parser.add_argument("-o", "--output", default="latency_stats_graph.png", help="Caminho para salvar o gráfico (opcional)")
args = parser.parse_args()

# Lista para armazenar os valores de latência de cada arquivo
all_latencies = []

# Regex para capturar "Overall Average latency: valor ms"
regex = r"Overall Average latency: ([\d\.]+) ms"

# Processar cada arquivo de log
for log_file_path in args.log_files:
    try:
        latencies = []
        with open(log_file_path, "r") as file:
            for line in file:
                match = re.search(regex, line)
                if match:
                    latencies.append(float(match.group(1)))
        all_latencies.append(latencies)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{log_file_path}' não encontrado.")
        exit(1)

# Garantir que há dados para processar
if not all_latencies:
    print("Nenhum dado de latência encontrado nos arquivos fornecidos.")
    exit(1)

# Transpor os dados para calcular estatísticas por índice
max_length = max(len(latencies) for latencies in all_latencies)
transposed_data = []
for i in range(max_length):
    transposed_data.append([latencies[i] for latencies in all_latencies if i < len(latencies)])

# Calcular média, máximo e mínimo para cada índice de request
means = [np.mean(values) for values in transposed_data]
max_values = [np.max(values) for values in transposed_data]
min_values = [np.min(values) for values in transposed_data]

# Gerar o gráfico
plt.figure(figsize=(12, 7))
plt.plot(means, marker="o", linestyle="-", label="Média", color="green")
plt.fill_between(range(len(means)), min_values, max_values, color="orange", alpha=0.2, label="Máximo e Mínimo")
plt.title("Estatísticas de Latência por Request")
plt.xlabel("Índice do Request")
plt.ylabel("Latência (ms)")
plt.legend()
plt.grid(True)

# Salvar o gráfico como imagem
output_image_path = args.output
plt.savefig(output_image_path)
plt.close()

print(f"Gráfico salvo em: {output_image_path}")
