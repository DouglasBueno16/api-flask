# API Flask

Esse repositório é utilizado para criar um api em `Python 3.12.3`.

Objetivo será ter uma api simples, para ser utilizado como estudo para:
- Criação de um Dockerfile
- Utilização das Github Actions
- Pipelines CI/CD 


## Instalação local

1. Faça um clone do repositório com `git clone` ou download como `.zip`
2. Instale as dependências com:
```bash
pip install -r requirements.txt
```
3. Inicie o programa com `python main.py`
4. Para inserir um usuário na api:
```bash
curl -X POST http://localhost:5000/users \
     -H "Content-Type: application/json" \
     -d '{"name": "User", "email": "user@email.com"}'
```
5. Listar usuário com `localhost:5000/users`
6. Deletar usuário `localhost:5000/delete/<id do usuário>`

## Próximos passos

- Adicionar um banco de dados para persistência
- Alteração no `pipeline.yaml` para enviar a imagem Docker para o Docker Hub
- Utilizar uma estrutura cloud para a aplicação
