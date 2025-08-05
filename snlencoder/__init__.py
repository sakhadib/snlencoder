"""
SNL Encoder - A package for encoding and decoding game moves.
"""

from .encode import encode_move, decode_move, batch_decode

__version__ = "1.0.0"
__author__ = "sakhadib"
__all__ = ["encode_move", "decode_move", "batch_decode"]
