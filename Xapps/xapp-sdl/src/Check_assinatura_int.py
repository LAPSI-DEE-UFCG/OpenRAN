import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Função para carregar chave pública de um arquivo
def carregar_chave_publica(nome_arquivo):
    with open(nome_arquivo, "rb") as f:
        chave_bytes = f.read()
        public_key = serialization.load_pem_public_key(
            chave_bytes,
            backend=default_backend()
        )
    return public_key

# Função para carregar assinatura de um arquivo
def carregar_assinatura(nome_arquivo):
    with open(nome_arquivo, "rb") as f:
        assinatura = f.read()
    return assinatura


def calcular_hash_arquivo(nome_arquivo):
    hash_sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
    with open(nome_arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            hash_sha256.update(bloco)
    return hash_sha256.finalize()

def calcular_hash_diretorio(diretorio):
    hash_total = hashes.Hash(hashes.SHA256(), backend=default_backend())
    for pasta_atual, _, arquivos in os.walk(diretorio):
        for nome_arquivo in arquivos:
            caminho_completo = os.path.join(pasta_atual, nome_arquivo)
            hash_arquivo = calcular_hash_arquivo(caminho_completo)
            hash_total.update(hash_arquivo)
    return hash_total.finalize()


def verificar_assinatura(public_key, assinatura, dados):
    try:
        public_key.verify(
            assinatura,
            dados,
            ec.ECDSA(utils.Prehashed(hashes.SHA256()))
        )
        return True
    except Exception as e:
        print(f"Erro ao verificar a assinatura: {e}")
        return False

nome_arquivo_chave_publica = "/etc/assigned-xapps/chave_publica_sdl.pem"
public_key_carregada = carregar_chave_publica(nome_arquivo_chave_publica)


# Exemplo de uso:
nome_arquivo_assinatura = "/etc/assigned-xapps/assinatura_sdl.bin"
assinatura_carregada = carregar_assinatura(nome_arquivo_assinatura)


diretorio = "/tmp"

# Verificar a assinatura
def Resposta():
    if verificar_assinatura(public_key_carregada, assinatura_carregada, calcular_hash_diretorio(diretorio)):
        return "Assinatura verificada com sucesso."
    else:
        return "Falha na verificação da assinatura!!!"