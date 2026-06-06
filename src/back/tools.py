import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
class Tools:
        
    @staticmethod
    def generate_verification_code() -> str:
        code = f"{secrets.randbelow(10000):04d}"
        return code
    
    @staticmethod
    def hash_password(password: str) -> str:
        return ph.hash(password)
    
    @staticmethod
    def verify_password(stored_hash: str, provided_password: str) -> bool:
        try:
            ph.verify(stored_hash, provided_password)
            return True
        
        except VerifyMismatchError:
            return False
        
        except Exception as _ex:  
            raise RuntimeError("Cant match passwords") from _ex
    

