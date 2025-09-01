import os
import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Exportar a chave pública para um arquivo
def exportar_chave_publica(public_key, nome_arquivo):
    with open(nome_arquivo, "wb") as f:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        f.write(pem)


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

def assinar_dados(private_key, dados):
    assinatura = private_key.sign(
        dados,
        ec.ECDSA(utils.Prehashed(hashes.SHA256()))
    )
    return assinatura

# Exportar a assinatura para um arquivo
def exportar_assinatura(assinatura, nome_arquivo):
    with open(nome_arquivo, "wb") as f:
        f.write(assinatura)


# Diretório a ser assinado 
diretorio = "/tmp"
# Calcular o hash do diretório
hash_diretorio = calcular_hash_diretorio(diretorio)
    
# Gerar par de chaves ECDSA P-256
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
public_key = private_key.public_key()


# Assinar o hash do diretório
assinatura = assinar_dados(private_key, hash_diretorio)

exportar_chave_publica(public_key, "/etc/assigned-xapps/chave_publica_sdl.pem")
comando = ["chmod", "-R", "444", "/etc/assigned-xapps/chave_publica_sdl.pem"]
subprocess.run(comando, check=True)

exportar_assinatura(assinatura, "/etc/assigned-xapps/assinatura_sdl.bin")
comando = ["chmod", "-R", "444", "/etc/assigned-xapps/assinatura_sdl.bin"]
subprocess.run(comando, check=True)

