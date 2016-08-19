Quickstart Python + MongoDB no Openshift
=============================

Este repositório possui uma aplicação python que utiliza o framework bottle e o MongoDB, e que está pronta para ser utilizada localmente e no Openshift. Além disso, está implementada a funcionalidade de autenticação utilizando JWT.

Para rodar localmente:

1. Clone este repositório

2. Instale os requisitos em requirements.txt

3. rode o script app.py, localizado na raiz.

4. Acesse http://localhost:8080/. Se tudo deu certo, aparecerá "Boa sorte!"


Para rodar este projeto no openshift:

1. Crie uma conta em https://www.openshift.com

2. Crie uma aplicação python-3.3 em openshift.com.

	2.1 Na opção "Source Code" em "Optional URL to a GIT repository" coloque o endereço deste repositório: https://github.com/du2x/simplerestaurant

3. Adicione um cartucho Mongodb para o app.

4. Acesse    http://appname-namespace.rhcloud.com/. Se tudo deu certo, aparecerá "Boa sorte!"


