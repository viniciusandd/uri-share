# Share!

A **Share!** é uma "micro rede social" empresarial, (ironicamente) desenvolvida utilizando o microframework [Flask](https://github.com/pallets/flask). Ela foi feita para a disciplina de Engenharia de Software III, onde seu objetivo principal era fornecer um ambiente de troca de experiência e conhecimento entre empresas.

## Como executar o projeto

Primeiramente, vamos criar um ambiente virtual (afinal, não querendo bagunçar seu ambiente de dev).

`python3 -m venv venv`

Inicie-o.

`source venv/bin/activate`

Agora que estamos com o ambiente iniciado, vamos instalar as dependências.

`pip install -r requirements.txt`

Vamos iniciar nosso repositório de migrações. Mais informações sobre o Flask-Migrate em: https://flask-migrate.readthedocs.io/en/latest/

`python3 run.py db init`

Gerando nossas migrações e criando o banco de dados sqlite (storage.db) na raíz.

`python3 run.py db migrate`

Aplicando as migrações no banco de dados.

`python3 run.py db upgrade`

Momentaneamente, não existe nada que insira automaticamente paises, estados e cidades. Possivelmente, essa feature logo será adicionada. Para testar, execute os seguintes scripts em seu SGDB favorito.

```
INSERT INTO `paises` (id, nome)
VALUES (1, 'Brasil');

INSERT INTO `estados` (id, nome, sigla, pais_id)
VALUES (1, 'Rio Grande do Sul', 'RS', 1);

INSERT INTO `cidades` (id, nome, estado_id)
VALUES (1, 'Erechim', 1);
```

Agora, o projeto está pronto para ser iniciado. 

`python3 run.py runserver`

Para acessar a página de login, abra seu navegador e digite:

`http://127.0.0.1:5000/`

