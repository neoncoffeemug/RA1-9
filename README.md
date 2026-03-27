## RA1 - Construção de Interpretadores

Pontífica Universidade Católica do Paraná

Professor: Frank Coelho de Alcantara

Alunos:

Lucas Ricardo Nagano Rigon - [neoncoffeemug](https://github.com/neoncoffeemug)       
Vinicius Mizuguchi Pagani - [ViniPagani](https://github.com/ViniPagani)


Estrutura do projeto:
```
projeto/
├── src/          
    ├── main.py
    ├── parseExpressao.py
    ├── executarExpressao.py
    ├── exibirResultados.py
    ├── gerarAssembly.py
    ├── lerArquivo.py
    ├── salvarTokens.py
├── tests/
    ├── test1.txt
    ├── test2.txt
    ├── test3.txt       
├── output/
    ├── programa.s
    ├── tokens.txt
├── README.md          
```
## Descrição do Projeto
Esse trabalho tem o objetivo de implementar um análisador léxico em pyton que recebe um arquivo .txt, análisa suas linhas, as transforma em tokens, faz validações léxicas e por fim traduz esse resultado para assembly ARMv7.


## Execução do Programa
Para executar o programa, no terminal root do projeto digite ```python3 src/main.py tests/test1.txt```. Isso gera dois arquivos, ```tokens.txt```, que é usado apenas para vizualização e ```programa.s``` que contem as instruções assembly.


## Testar o Programa
Com o arquivo gerado acesse o site do [cpulator](https://cpulator.01xz.net/?sys=arm-de1soc&d_audio=48000) (aqui já selecionado para armv7). Vá na caixa ```file``` , selecione ```open``` e selecione o arquivo gerado ```programa.s```.\
Aperte F5 para compilar e carregar o arquivo, aperte F3 para continuar a execução. Na esquerda, em ajustes troque a exibição de número hexadecimal para decimal signed, isso atualiza a exibição dos elementos nos registradores.

