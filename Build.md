# Construindo, instalando e verificando os xAPPs

#1° Passo 

No cluster Kubernetes Near-RT RIC da OSC, cada xApp é implantado como um pod, que pode conter um ou mais contêineres Docker e um conjunto de serviços, responsáveis por expor as portas abertas do pod. As informações necessárias para construir o pod e seus serviços são definidas no descritor do xApp, conhecido como config-file (opcional). Para garantir a correção da sintaxe da seção de controle,  um arquivo de esquema pode acompanhar o config-file.
Ambos os arquivos são do tipo ** .json **
