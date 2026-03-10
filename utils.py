import string

ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

class Base62Encoder:
    @staticmethod
    def encode(n: int) -> str:
        if n == 0: return ALPHABET[0]
        res = []
        while n:
            n, rem = divmod(n, 62)
            res.append(ALPHABET[rem])
        return "".join(reversed(res))

    @staticmethod
    def decode(short_id: str) -> int | None:
        try:
            n = 0
            for char in short_id:
                n = n * 62 + ALPHABET.index(char)
            return n
        except (ValueError, IndexError):
            return None
