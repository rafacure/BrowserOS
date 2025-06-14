import subprocess

def get_dependencies(package):
    # Executa o comando repoquery para obter as dependências do pacote, filtrando mensagens de metadados
    result = subprocess.run(['repoquery', '--requires', '--resolve', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dependencies = result.stdout.decode('utf-8').strip().split('\n')
    return [dep for dep in dependencies if dep]

def main(packages):
    all_packages = set(packages)  # Inicializa o conjunto com os pacotes fornecidos
    to_process = set(packages)    # Inicializa o conjunto com os pacotes a processar
    processed = 0  # Contador para pacotes processados

    print("Progresso: |", end="", flush=True)

    while to_process:
        package = to_process.pop()
        dependencies = get_dependencies(package)
        for dep in dependencies:
            if dep not in all_packages:
                all_packages.add(dep)
                to_process.add(dep)
        
        # Atualiza a barra de progresso com menos frequência
        processed += 1
        if processed % 10 == 0:
            print("|", end="", flush=True)

    # Adiciona uma linha de nova linha após a barra de progresso
    print()
    
    sorted_packages = sorted(all_packages)
    for pkg in sorted_packages:
        print(pkg)

if __name__ == '__main__':
    # Substitua 'package1', 'package2', 'package3' pelos nomes dos pacotes que você quer informar
    initial_packages = ['package1', 'package2', 'package3']
    main(initial_packages)

