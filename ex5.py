import os
import json


class CaesarCipher:
    ascciLetters = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
        'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
        'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
        'y': 24, 'z': 25,
        'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33,
        'I': 34, 'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41,
        'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49,
        'Y': 50, 'Z': 51
    }

    def _init_(self, num):
        self.cypher = num % 26

    def shift_right(self, str):
        newWord = ""
        for c in str:
            if c in self.ascciLetters and self.ascciLetters[c] < 26:
                x = ((self.ascciLetters[c] + self.cypher) % 26)
                for letter, value in self.ascciLetters.items():
                    if (value == x):
                        newWord += letter
                        break
            elif c in self.ascciLetters and self.ascciLetters[c] > 25 and self.ascciLetters[c] < 52:
                x = ((self.ascciLetters[c] + self.cypher) % 26) + 26
                for letter, value in self.ascciLetters.items():
                    if (value == x):
                        newWord += letter
                        break
            else:
                newWord += c
        return newWord

    def shift_left(self, str):
        self.cypher = -self.cypher
        newWord = self.shift_right(str)
        self.cypher = -self.cypher
        return newWord

    def encrypt(self, str):
        return self.shift_right(str)

    def decrypt(self, str):
        return self.shift_left(str)

    def key_shift(self, num):
        self.cypher += num


class VigenereCipher:
    ascciLetters = {
        'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
        'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15,
        'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
        'y': 24, 'z': 25,
        'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33,
        'I': 34, 'J': 35, 'K': 36, 'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41,
        'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47, 'W': 48, 'X': 49,
        'Y': 50, 'Z': 51
    }

    def _init_(self, list1):
        self.list = []
        for x in list1:
            self.list.append(x)

    def shift(self, str):
        i = 0
        newWord = ""
        for c in str:
            if c in self.ascciLetters and self.ascciLetters[c] < 26:
                x = ((self.ascciLetters[c] + self.list[i]) % 26)
                i += 1
                if i == len(self.list):
                    i = 0
                for letter, value in self.ascciLetters.items():
                    if (value == x):
                        newWord += letter
                        break
            elif c in self.ascciLetters and self.ascciLetters[c] > 25 and self.ascciLetters[c] < 52:
                x = ((self.ascciLetters[c] + self.list[i]) % 26) + 26
                i += 1
                if i == len(self.list):
                    i = 0
                for letter, value in self.ascciLetters.items():
                    if (value == x):
                        newWord += letter
                        break
            else:
                newWord += c
        return newWord

    def encrypt(self, str):
        return self.shift(str)

    def decrypt(self, str):
        for i in range(len(self.list)):
            self.list[i] = -self.list[i]
        newWord = self.encrypt(str)
        for i in range(len(self.list)):
            self.list[i] = -self.list[i]
        return newWord


def loadEncryptionSystem(dir_path, plaintext_suffix):
    folder = os.listdir(dir_path)
    if not dir_path == '.':
        os.chdir(dir_path)
    config_file_path = os.path.join(dir_path, 'config.json')
    with open(config_file_path, 'r') as file:
        data = json.load(file)
        if data["type"] == 'Vigenere':
            if "key" in data and isinstance(data["key"], list):
                type1 = VigenereCipher(data["key"])
            else:
                print("Error: 'key' field is missing or not a list in the JSON data.")
        elif data["type"] == 'Caesar':
            type1 = CaesarCipher(data["key"])
        crypt = data["encrypt"]

    for file in folder:
        if crypt == "True":
            if (not file.endswith(plaintext_suffix)):
                continue
            str = file.replace(plaintext_suffix,"enc")
            os.mkdir(str)
            with open(str, "w") as writeto:
                with open(file, "w") as current:
                    to_encrypt = current.read()
                    encrypted = type1.encrypt(to_encrypt)
                    writeto.write(encrypted)
        else:
                if(not file.endswith(".enc")):
                    continue
                str = file.replace("enc",plaintext_suffix)
                os.mkdir(str)
                with open(str, "w") as writeto:
                     with open(file, "w") as readfrom:
                         to_decrypt = file.read()
                         decrypted = type1.decrypt(to_decrypt)
                         writeto.write(decrypted)