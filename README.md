# Symmetric-Cryptography

A Python implementation of the AES (Advanced Encryption Standard) decryption algorithm with detailed module breakdown for educational purposes.

## Overview

This project provides a complete implementation of AES-128 decryption, breaking down the algorithm into its core components. AES is a widely-used symmetric encryption standard that processes data in 128-bit blocks using a 128-bit key (for AES-128) through 10 rounds of transformations.

## Project Structure

The project is organized into modular components, each implementing specific AES operations:

### Core Modules

- **`aes_decrypt.py`** - Main decryption engine
  - Implements the complete AES-128 decryption algorithm
  - Handles key expansion and round-based decryption
  - Coordinates all transformation steps
  - Entry point for decrypting ciphertext

- **`sbox.py`** - Substitution Box Implementation
  - Contains S-box and inverse S-box lookup tables
  - Implements `sub_bytes()` function for byte substitution using the inverse S-box
  - Critical for the non-linear transformation in AES

- **`diffusion.py`** - Diffusion Transformations
  - `shift_rows()` - Performs cyclic row shifts on the state matrix
  - `inv_shift_rows()` - Inverse operation for row shifting
  - `mix_columns()` and `mix_single_column()` - Linear mixing of column data
  - Provides diffusion to spread the effect of single bits across the data

- **`add_round_key.py`** - Round Key Addition
  - Implements `add_round_key()` function
  - Performs XOR operation between state and round key
  - Applied after key expansion and between rounds

- **`matrix.py`** - Utility Functions
  - `bytes2matrix()` - Converts 16-byte arrays to 4×4 matrices
  - `matrix2bytes()` - Converts 4×4 matrices back to byte arrays
  - Helper functions for data format conversion

## How AES Decryption Works

AES decryption reverses the encryption process through the following steps:

1. **Key Expansion** - Expands the 128-bit master key into 11 round keys (10 rounds + initial)
2. **Initial Round** - XOR ciphertext with the last round key
3. **Main Rounds (9 rounds)** - For each round, apply in reverse order:
   - Inverse Shift Rows
   - Inverse Substitute Bytes (using inverse S-box)
   - Add Round Key
   - Inverse Mix Columns
4. **Final Round** - Skip Mix Columns step and perform:
   - Inverse Shift Rows
   - Inverse Substitute Bytes
   - Add Round Key

## Usage

### Basic Decryption

```python
from aes_decrypt import decrypt

# 128-bit key (16 bytes)
key = b'\xc3,\\\xa6\xb5\x80^\x0c\xdb\x8d\xa5z*\xb6\xfe\\'

# 128-bit ciphertext (16 bytes)
ciphertext = b'\xd1O\x14j\xa4+O\xb6\xa1\xc4\x08B)\x8f\x12\xdd'

# Decrypt
plaintext = decrypt(key, ciphertext)
print(plaintext)
```

### Testing Individual Components

```python
# Test S-box substitution
from sbox import sub_bytes, state

result = sub_bytes(state, sbox=inv_s_box)
print(result)

# Test add_round_key
from add_round_key import add_round_key

state = [[206, 243, 61, 34], ...]
round_key = [[173, 129, 68, 82], ...]
result = add_round_key(state, round_key)
```

## Technical Details

### Data Representation

- **State Matrix** - 4×4 matrix of bytes representing the current data being processed
- **Round Keys** - Derived from the master key through key expansion
- **Block Size** - 128 bits (16 bytes)
- **Key Size** - 128 bits (16 bytes for AES-128)
- **Number of Rounds** - 10 for AES-128

### Key Operations

| Operation | Purpose |
|-----------|---------|
| SubBytes | Non-linear byte-level substitution |
| ShiftRows | Circular rotation of matrix rows |
| MixColumns | Linear transformation of matrix columns |
| AddRoundKey | XOR with round key material |
| KeyExpansion | Generate round keys from master key |

## Requirements

- Python 3.x
- No external dependencies

## References

- [AES Specification (FIPS 197)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [The Design of Rijndael](https://www.springer.com/gp/book/9783540425809)
- AES Round Constants and S-box values follow the official NIST standard

## Educational Purpose

This implementation is designed for educational purposes to understand how AES decryption works at a fundamental level. Each module isolates specific operations, making it easier to study individual components of the algorithm.

## Notes

- This is an AES-128 decryption implementation (10 rounds)
- The code uses the standard AES S-box and inverse S-box values
- Key expansion follows the AES key schedule algorithm
- Not optimized for production use; focus is on clarity and education