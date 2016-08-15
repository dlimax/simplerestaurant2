Python 3.3 + Bottle running at Openshift
=============================

1. Crie uma conta em https://www.openshift.com

2. Crie um fork deste repositório.

3. Clone para a sua máquina  o repositório que você acabou de criar com o fork.

```bash  
 git clone <github-repo-url>
```

4. Adicione o repositório Openshift como remote para o seu clone 
```bash
 git remote add openshift -f <openshift-git-repo-url>
```

5. Para realizar pushes, primeiro você precisa mesclar seu repositório do openshift com o do seu clone do github. Você faz isso assim:
```bash
git merge openshift/master -s recursive -X ours
```

6. Quando a mesclagem (merge) estiver pronto, você estará pronto para atualizar o seu repositório openshift.

```bash
git push openshift HEAD
```

7. Crie uma aplicação python-3.3 em openshift.com.

	7.1 Na opção "Source Code" em "Optional URL to a GIT repository" coloque o endereço de seu repositório GIT"

8. Adicione um cartucho Mongodb para o app.

9. Acesse    http://<app name>-<your namespace>.rhcloud.com/. Se tudo deu certo, aparecerá "Boa sorte!"
