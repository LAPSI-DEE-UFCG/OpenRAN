# Guia de Deploy de xApp no Near-RT RIC

Este guia descreve o passo a passo para **onboard, build, push e instalar xApps** no cluster Kubernetes Near-RT RIC da OSC.

---

## 1. Onboard do xApp

Antes de construir o container, faça o **onboard** do xApp usando o **DMS CLI**. Isso registra o xApp no sistema.

```bash
dms_cli onboard <CONFIG_FILE_PATH> <SCHEMA_PATH>
```

* `<CONFIG_FILE_PATH>`: Caminho para o **config-file** do xApp (`.json`).
* `<SCHEMA_PATH>`: Caminho para o **arquivo de esquema** que valida o config-file (`.json`).

---

## 2. Listar charts disponíveis

Para verificar os charts disponíveis no DMS, execute:

```bash
dms_cli get_charts_list
```

Isso ajuda a confirmar se o xApp foi onboard corretamente.

---

## 3. Construir a imagem Docker do xApp

No diretório raiz do xApp, construa a imagem Docker:

```bash
docker build . -t 127.0.0.1:5001/<XAPP_NAME>:<XAPP_VERSION> --network host
```

* `<XAPP_NAME>`: Nome do xApp.
* `<XAPP_VERSION>`: Versão do xApp.
* `--network host`: Permite que o build use a rede do host, útil para conexões internas.

Verifique se a imagem foi criada corretamente:

```bash
docker images
```

---

## 4. Enviar a imagem para o repositório local

Após a construção, envie a imagem Docker para o repositório:

```bash
docker push <REPOSITORY>:<TAG>
```

* `<REPOSITORY>`: Endereço do repositório (ex: `127.0.0.1:5001/<XAPP_NAME>`).
* `<TAG>`: Versão do xApp (ex: `v1.0.0`).

---

## 5. Instalar o xApp no cluster

Com a imagem disponível no repositório, instale o xApp no **namespace** desejado:

```bash
dms_cli install <XAPP_NAME> <XAPP_VERSION> <NAMESPACE>
```

* `<NAMESPACE>`: Namespace Kubernetes onde o xApp será executado.

---

## 6. Debug: Verificar pods e serviços

Para conferir se o xApp está rodando e as portas estão abertas, use os comandos abaixo:

```bash
kubectl -n <NAMESPACE> get pods    # Lista os pods do namespace
kubectl -n <NAMESPACE> get svc     # Lista os serviços e portas abertas
```

---

## 7. Desinstalar o xApp

Se necessário, o xApp pode ser removido do cluster com:

```bash
dms_cli uninstall <XAPP_NAME> <NAMESPACE>
```

---

## Observações

* Certifique-se de que o **Docker** e o **DMS CLI** estão configurados corretamente no seu ambiente.
* Os caminhos para config-file e schema devem estar acessíveis no host onde o comando é executado.
* Recomenda-se sempre verificar os **logs do pod** no Kubernetes para confirmar que o xApp está rodando corretamente.

---

## Estrutura do xApp no Near-RT RIC

No **cluster Kubernetes Near-RT RIC da OSC**, cada **xApp** é implantado como um **pod**, que pode conter **um ou mais contêineres Docker** e um conjunto de **serviços**, responsáveis por expor as portas abertas do pod. As informações necessárias para construir o pod e seus serviços são definidas no **descritor do xApp**, conhecido como **config-file** (opcional).

Para garantir a correção da sintaxe da seção de controle, um **arquivo de esquema** pode acompanhar o config-file. Ambos os arquivos são do tipo **.json** e normalmente estão localizados dentro do diretório **init/**.
