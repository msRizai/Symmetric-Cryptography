# Symmetric-Cryptography

Solutions in Python to the [CryptoHack – Symmetric Cryptography](https://cryptohack.org/courses/symmetric/) course: a from-scratch AES-128 decryption, built step by step, and attacks against the ECB and CBC block cipher modes.

## Overview

The repository covers two parts of the course:

1. **How AES works** – each step of AES (SubBytes, ShiftRows, MixColumns, AddRoundKey, key expansion) is written by hand, then all the steps are put together into a full AES-128 decryption.
2. **Attacking block cipher modes** – scripts that talk to the CryptoHack challenge servers (`aes.cryptohack.org`) to break bad uses of ECB and CBC.

## Project Structure

### Part 1 – How AES works

| File | Contents |
|------|----------|
| [`matrix.py`](matrix.py) | `bytes2matrix()` / `matrix2bytes()`: convert between 16 bytes and the 4×4 AES state |
| [`add_round_key.py`](add_round_key.py) | `add_round_key()`: byte-by-byte XOR of the state with a round key |
| [`sbox.py`](sbox.py) | `s_box` / `inv_s_box` tables and `sub_bytes()` (uses `s_box` by default, `inv_s_box` to decrypt) |
| [`diffusion.py`](diffusion.py) | `shift_rows()`, `inv_shift_rows()`, `mix_columns()`, `inv_mix_columns()` |
| [`aes_decrypt.py`](aes_decrypt.py) | `expand_key()` (key schedule) and `decrypt()`: full 10-round AES-128 decryption |

### Part 2 – Attacking block cipher modes

| File | Challenge | Attack |
|------|-----------|--------|
| [`ecb_oracle.py`](ecb_oracle.py) | **ECB Oracle** | Recovers the flag one byte at a time. In ECB, identical plaintext blocks give identical ciphertext blocks, so a guessed block is compared with the block that holds the unknown flag byte. |
| [`ecb_cbc_wtf.py`](ecb_cbc_wtf.py) | **ECB CBC WTF** | The flag is encrypted in CBC, but the server decrypts in ECB. Each block is decrypted with ECB and XORed with the previous ciphertext block (the IV for the first one), which redoes CBC decryption by hand. |
| [`flipping_cookies.py`](flipping_cookies.py) | **Flipping Cookie** | CBC bit-flipping: a forged IV and changes to the first ciphertext block turn `admin=False` into `admin=True` without knowing the key. |

## How AES Decryption Works

`decrypt()` in `aes_decrypt.py` runs the AES steps in reverse:

1. **Key expansion** – the 128-bit key becomes 11 round keys.
2. **Initial step** – XOR the ciphertext with the last round key.
3. **Rounds 9 → 1** – `InvShiftRows` → `InvSubBytes` → `AddRoundKey` → `InvMixColumns`.
4. **Last round** – same as the others but without `InvMixColumns`.

| Operation | Purpose |
|-----------|---------|
| SubBytes | Non-linear substitution of each byte (confusion) |
| ShiftRows | Circular shift of the state rows (diffusion) |
| MixColumns | Linear mixing of each column in GF(2⁸) (diffusion) |
| AddRoundKey | XOR with the round key |
| KeyExpansion | Builds the round keys from the master key |

## Usage

Each file is a standalone script that prints its result when run:

```bash
# Part 1 – AES
python3 aes_decrypt.py        # decrypts the challenge ciphertext and prints the flag
python3 sbox.py
python3 diffusion.py
python3 add_round_key.py

# Part 2 – attacks (need Internet access to aes.cryptohack.org)
python3 ecb_oracle.py
python3 ecb_cbc_wtf.py
python3 flipping_cookies.py
```

> Note: the Part 1 modules print the challenge results at the top level. Importing them (e.g. `from aes_decrypt import decrypt`) also prints these results.

## Requirements

- Python 3.9+
- [`requests`](https://pypi.org/project/requests/) for the Part 2 scripts:

```bash
pip install requests
```

## References

- [CryptoHack – Symmetric Cryptography](https://cryptohack.org/courses/symmetric/)
- [AES Specification (FIPS 197)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf)
- [The Design of Rijndael](https://link.springer.com/book/10.1007/978-3-662-60769-5)
- [Block cipher modes of operation (Wikipedia)](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation)

## Disclaimer

This code is for learning only. It is not optimized or hardened and must not be used to protect real data. The attack scripts only target the CryptoHack challenge servers, which exist for this purpose.
