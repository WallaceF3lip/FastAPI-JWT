from passlib.context import CryptContext
import hashlib

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Func utilizada para verificar se a senha fornecida corresponde ao hash armazenado.
    """
    # Aplica SHA256 antes de verificar
    password_hash = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return CRIPTO.verify(password_hash, hashed_password)

def generate_hashed_password(password: str) -> str:
    """
    Func utilizada para gerar um hash seguro para a senha fornecida.
    """
    # Primeiro aplica SHA256 para normalizar o tamanho
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    # Depois aplica bcrypt
    return CRIPTO.hash(password_hash)