import os
import sys
import shutil

from vigenere import Vigenere


def read_all_files_data(path):
    result = ''
    all_files = []
    for elem in os.walk(path):
        path, _, files = elem

        for filepath in files:
            f = open(path + '/' + filepath, 'r', encoding='utf-8')
            all_files.append(f'{path + "/" + filepath}^{f.read()}')

    return '@'.join(all_files)


def replace_dir_content_with_encoded_file(path, vigenere_model: Vigenere):
    with open('.fileinfo', 'w', encoding='utf-8') as out:
        vigenere_model.encode_message()

        out.write(vigenere_model.encoded_text)

        shutil.rmtree(path)


def replace_encoded_file_with_dirtree(vigenere_model: Vigenere):
    vigenere_model.decode_message()
    files_data = vigenere_model.text

    d = {}
    for file_data in files_data.split('@'):
        data = file_data.split('^')
        d[data[0]] = data[1]

    for filepath, file_content in d.items():
        path_parts = filepath.split('/')
        filename = path_parts.pop()

        for idx in range(len(path_parts)):
            if not os.path.exists('/'.join(path_parts[0:idx + 1])):
                os.mkdir('/'.join(path_parts[0:idx + 1]))

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(file_content)

    os.remove('.fileinfo')


def main():
    command = ''
    while True:
        print(
            """
                Введите команду для выполнения действия:
                1. Зашифровать директорию
                2. Расшифровать директорию
            """
        )
        command = input()
        if command == '1':
            print('Введите путь до директории:', end=' ')
            dirpath = input()
            if os.path.exists(dirpath):
                print('Введите ключ для шифрования:', end=' ')
                key = input()
                files_data = read_all_files_data(dirpath)
                vigenere = Vigenere(key, files_data, is_text_encoded=False)
                replace_dir_content_with_encoded_file(dirpath, vigenere)
            else:
                raise Exception('Директории по такому пути не существует')
        elif command == '2':
            print('Введите ключ для дешифрования:', end=' ')
            key = input()
            file_info = open('.fileinfo', 'r')
            encoded_data = file_info.read()
            file_info.close()

            vigenere = Vigenere(key, encoded_data, is_text_encoded=True)
            replace_encoded_file_with_dirtree(vigenere)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
