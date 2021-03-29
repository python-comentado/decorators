```python
# -*- coding: utf-8 -*-
from time import time

import requests


# Vamos inicialmente criar uma função que recebe o nome de um usuário
# do Github (www.github.com) e salva a foto de perfil desse usuário.
def save_image(username):
    # o primeiro passo dessa função é fazer uma chamada no endereço
    # que guarda a imagem de perfil de "username". Para isso usaremos
    # uma f-string, ou template string:
    url = f"https://www.github.com/{username}.png"
    response = requests.get(url)  # requisição do tipo GET na url
    # agora podemos salvar o conteúdo (content) da resposta acima
    # em um arquivo de image. Para isso, vamos usar f-string novamente:
    filename = f"{username}.png"
    # mode="wb+" é o modo de interação.
    # w -> write  (escrever)
    # b -> binary (binário)
    # + -> create (autoriza a criação do arquivo se ainda não existir)
    with open(filename, mode='wb+') as image_file:
        image_file.write(response.content)


# A simples chamada da função save_image("python-comentado") é
# capaz de gerar a imagem que você encontrará no final desse post. Apesar
# de estarmos lidando com requisições aqui, o objetivo deste post é
# exemplificar um uso bastante comum de um padrão de projeto (aqui podemos 
# interpretar como feature da linguagem) chamado# Decorator. Para fazer isso,
# vamos medir o tempo de execução da função acima. Para medir o tempo, basta 
# que seja feita a marcação do tempo de início, tempo de término e subtrair:
start = time()  # tempo de início
save_image("python-comentado")
end = time()  # tempo de término
# arredondamento de 3 casas decimais
print(f"Tempo gasto: {round(end - start, 3)} s")
# Tempo gasto 1.693 s
```

O exemplo anterior funciona, mas em qualquer projeto de tamanho razoável, seria desagradável ficar criando as variáveis `"start"` e `"end"` várias e várias vezes. Uma outra abordagem possível seria criar essas variáveis dentro da função `"save_image"`, mas isso também não seria legal, pois se quiséssemos medir o tempo de outras funções do programa, precisaríamos fazer a mesma coisa em todas elas: marcar tempo de início, tempo de término, subtrair e exibir o resultado. Vamos tentar fazer algo mais geral: uma função que recebe como argumento uma segunda função genérica e devolve esta última modificada, com a feature de medir tempo. Vejamos a seguir.

```python
# A função timeit recebe uma função qualquer e devolve uma segunda função que
# recebe todos os argumentos da primeira e que devolve o mesmo resultado da 
# primeira. Ou seja, se ela tem as mesmas entradas e a mesma saída, de certo
# modo, é a mesma função! A diferença é que entre o início e o fim da execução,
# alguns passos extras serão desenvolvidos.
def timeit(some_function):
    # A função abaixo é uma "envoltória". Ela repete os passos de
    # marcação do tempo e exibe o tempo no console/terminal. Além disso,
    # essa função "wrapper" repassa todos os argumentos 
    def wrapper(*args, **kwargs):
        start = time()
        result = some_function(*args, **kwargs)
        end = time()
        print(f"Tempo gasto: {round(end - start, 3)} s")
        return result
    # devolve a função interna criada que recebe como entrada
    # quaisquer que sejam as entradas de "some_function" e devolve
    # qualquer que seja a saída de "some_function"
    return wrapper

# Vamos testar utilizando a função que baixa imagem de perfil (já criada)
# Para isso, podemos salvar em uma variável:
modified_save_image = timeit(save_image)
# Antes de prosseguir, vamos ver o que é a variável "modified_save_image":
print(type(modified_save_image)) # <class 'function'>

# Se você testar, verá que a chamada a seguir faz exatamente o que queríamos:
# start no cronômetro, download da imagem, salvamento do arquivo, stop no 
# cronômetro e exibição do tempo gasto na operação.
modified_save_image("python-comentado")

# Se você chegou até aqui, talvez esteja se perguntando se tudo realmente
# deixa o código melhor ou se isso tudo é vantajoso, uma vez que tivemos que
# criar a variável "modified_save_image" e teríamos que criar uma para cada
# nova função com a feature de medir tempo. De fato, isso é também é 
# desagradável e não é tão vantajoso quanto esperávamos quando pensamos
# em fazer uma melhoria lá atrás. Pensando nisso, assim como em diversas outras
# linguagens de programação existe o padrão de Decorators. A função "timeit"
# definida acima é um Decorator simples que pode ser aplicado a qualquer
# função com um simples "@timeit" antes da definição, sem a necessidade de criar
# uma nova variável. Desse modo, tudo o que fizemos até aqui poderia 
# ser resumido em:

def timeit(some_function):
    def wrapper(*args, **kwargs):
        start = time()
        result = some_function(*args, **kwargs)
        end = time()
        print(f"Tempo gasto: {round(end - start, 3)} s")
        return result
    return wrapper

@timeit
def save_image(username):
    url = f"https://www.github.com/{username}.png"
    response = requests.get(url)  # requisição do tipo GET na url
    filename = f"{username}.png"
    with open(filename, mode='wb+') as image_file:
        image_file.write(response.content)

# Por fim, a chamada de save_image agora faz exatamente o que queríamos, sem a 
# necessidade de nenhuma "gambiarra" ou variável nova:
save_image("python-comentado") 
# Tempo gasto: 1.878 s
```