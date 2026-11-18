def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
        bytes = []
        for a in matrix:
                for j in a:
                        bytes.append(j);
        return "".join(chr(c) for c in bytes)

def int2str(bytes):
        str = ""
        for a in bytes:
                str += chr(a)
        return str

states = ['08ca01f50a792779', '2470244b44989ad7', '4dd99db6949b22af', 'e2fa7605b759a0bf', 'e44dd4155fa0af8d', '481b35c0e191c1be']