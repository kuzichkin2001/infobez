class Vigenere:
    def __init__(self, key: str, text: str, is_text_encoded: bool):
        self.key = key
        self.text = None
        self.encoded_text = None
        if not is_text_encoded:
            self.text = text
        else:
            self.encoded_text = text

    def _form_dict(self):
        self.d = {}
        itr = 0
        for i in range(0, 128):
            self.d[itr] = chr(i)
            itr = itr + 1

    def _encode_val(self, s):
        list_code = []
        lent = len(s)
        self._form_dict()

        for w in range(lent):
            for value in self.d:
                if s[w] == self.d[value]:
                    list_code.append(value)
        return list_code

    def encode_message(self):
        # munyaninyanyo
        # key: aboba
        message_codes = self._encode_val(self.text)
        key_codes = self._encode_val(self.key)

        key_idx = 0
        key_len = len(key_codes)

        alphabet_modulo = 128

        result = ''
        for code in message_codes:
            result += chr((code + key_codes[key_idx]) % alphabet_modulo)

            key_idx = (key_idx + 1) % key_len

        self.encoded_text = result
        self.text = None

    def decode_message(self):
        encoded_message_codes = self._encode_val(self.encoded_text)
        key_codes = self._encode_val(self.key)

        key_idx = 0
        key_len = len(key_codes)

        alphabet_modulo = 128

        result = ''
        for code in encoded_message_codes:
            result += (chr((code - key_codes[key_idx]) % alphabet_modulo))

            key_idx = (key_idx + 1) % key_len

        self.text = result
        self.encoded_text = None

