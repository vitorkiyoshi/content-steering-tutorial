import matplotlib.pyplot as plt

# Lista para armazenar os dados do arquivo
dados = []

# Ler dados do arquivo
with open("latency_average.txt", "r") as arquivo:
    for linha in arquivo:
        # Remover espaços em branco e converter para número
        dado = float(linha.strip())
        dados.append(dado)

# Gerar o gráfico
plt.figure(figsize=(20, 5))
plt.plot(dados, marker='o')  # 'marker' adiciona um marcador em cada ponto
plt.title("Average Latency")
plt.xlabel("Iteration")
plt.ylabel("Average Latency")
plt.ylim(0, 20)
plt.grid(True)

# Exibir o gráfico
plt.savefig("latency_average.png")