import subprocess
import hashlib
import base64
from loguru import logger
from .commands import get_derivation
import rfc8785

def get_canonical_derivation(path):
    """Get canonicalized JSON representation of a Nix derivation"""
    deriv_json = get_derivation(path)
    return rfc8785.dumps(deriv_json)

def compute_sha256_base64(data: bytes):
    """Compute SHA-256 hash and return URL-safe base64 encoded"""
    logger.debug(f"Input type: {type(data)}")
    logger.debug(f"Input data: {data}...")
    hash_bytes = hashlib.sha256(data).digest()
    result = base64.urlsafe_b64encode(hash_bytes).decode('ascii').rstrip('=')
    logger.debug(f"Computed hash: {result}")
    return result

def compute_derivation_input_hash(drv_path: str) -> str:
    """
    Compute the input hash for a derivation path.
    This is the central function that should be used by both signing and verification.
    """
    canonical = get_canonical_derivation(drv_path)
    return compute_sha256_base64(canonical)
