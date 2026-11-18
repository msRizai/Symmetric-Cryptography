import requests

BASE_URL = "https://aes.cryptohack.org/ecbcbcwtf"


def get_encrypted_flag():
    """Récupère le flag chiffré en CBC (format : IV + ciphertext, en hex)."""
    r = requests.get(f"{BASE_URL}/encrypt_flag/")
    return bytes.fromhex(r.json()["ciphertext"])


def decrypt_ecb(block):
    """Envoie des données au serveur, qui les déchiffre en mode ECB."""
    r = requests.get(f"{BASE_URL}/decrypt/{block.hex()}/")
    return bytes.fromhex(r.json()["plaintext"])


def ECB_decrypt(bloc: list[int]) -> list[int]:
    """Adaptation : passe par le serveur pour déchiffrer un bloc en ECB."""
    return list(decrypt_ecb(bytes(bloc)))


def traiter(donnees: list[int]) -> list[int]:

    resultats = []
    for i in range(16, len(donnees), 16):
        bloc = donnees[i:i + 16]  # bloc courant
        precedent = donnees[i - 16:i]  # 16 octets precedents
        sortie = ECB_decrypt(bloc)  # decyptage
        resultats += [a ^ b for a, b in zip(sortie, precedent)]  # fait le XOR element par element et ajoute a la suite du resultat

    return resultats


def solve():
    data = get_encrypted_flag()

    flag = bytes(traiter(list(data)))

    print(flag)
    return flag


if __name__ == "__main__":
    solve()
