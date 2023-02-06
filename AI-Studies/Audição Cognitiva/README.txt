Trabalho Final de Audição Cognitiva - FIAP 2023 - Prof. Alexandre Gastaldi Lopes Fernandes

1. O desafio
	Criar um sistema de geração e reconhecimento de voz, para transferir um atendente entre quatro setores: Vendas, Administrativo, Financeiro e Aluguel. O usuário responde então e, conforme compreensão da máquina é gerada uma resposta indicando a transferência
2. Funcionamento, Desenvolvimento e Diferenciais
	Buscou-se fazer uma entrega que não dependa de API's ou conexão à Internet. O trabalho inteiro pode ser rodado baixando a pasta do GitHub, gerando um ambiente virtual (preferencialmente) e instalando as dependências com 'pip install -r requirements.txt'. 
	Usou-se a biblioteca Vosk para detecção de fala, por possuir um modelo pequeno (50mb) em português que reconheça as palavras-chave exigidas, e o pyttsx3 para gerar fala em Português.
	O processo tem duas fases: Apresentação da atendente,randomizando nomes em uma lista e perguntando para qual área o usuário deseja ser transferido, e um momento de resposta, no qual o usuário define para onde quer ir.
	A consulta é feita, então, obtendo o resultado do texto falado pelo usuário (output do Vosk), quebrado por espaço (buscando palavras individuais) e batendo estas com as possibilidades de transferência.
	Se nenhuma das quatro palavras-chave forem ditas, o processo pergunta novamente e, se o mesmo ocorrer, o atendente encerra o contato.
	Além do mais, por solicitação do professor, foram implementadas algumas palavras para sair do atendimento: 'tchau', 'desligar', 'encerrar', 'bye', 'sair'.
3. Problemas conhecidos: 
	- Existe uma demora maior na primeira execução do algoritmo, pelo pyttsx3 estar carregando o necessário para gerar as vozes.
4. Vídeo Demonstrativo - https://youtu.be/veRWqotWWm4