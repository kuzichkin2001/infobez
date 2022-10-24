# alexgrt@yandex.ru

FROM_RUSSIAN_TO_ENGLISH_LETTERS = {
    'а': 'a',
    'о': 'o',
    'у': 'y',
    'е': 'e',
    'р': 'p',
    'с': 'c',
    'х': 'x',
    'А': 'A',
    'В': 'B',
    'Е': 'E',
    'К': 'K',
    'О': 'O',
    'Р': 'P',
    'С': 'C',
    'Т': 'T',
    'Х': 'X',
    'Н': 'H',
    'М': 'M'
}


def read_from_container(filename: str):
    with open(filename, 'r', encoding='utf-8') as container_file:
        file_data = container_file.read()

        return file_data


def encode_message_into_stegocontainer(message: str, filename: str, stego_filename: str):
    container_data = list(read_from_container(filename))

    binary_message = bin(int.from_bytes(message.encode('windows-1251', 'surrogatepass'), 'big'))[2:]
    binary_message = binary_message.zfill(8 * ((len(binary_message) + 7) // 8))
    print(f'binary message during encoding: {binary_message}')

    message_index = 0
    message_len = len(binary_message)
    cindx = 0
    while message_index != message_len and cindx != len(container_data):
        if container_data[cindx] in FROM_RUSSIAN_TO_ENGLISH_LETTERS.keys() or container_data[cindx] in FROM_RUSSIAN_TO_ENGLISH_LETTERS.values():
            if binary_message[message_index] == '1':
                container_data[cindx] = FROM_RUSSIAN_TO_ENGLISH_LETTERS[container_data[cindx]]
            message_index += 1
        cindx += 1

    with open(stego_filename, 'w', encoding='utf-8') as stego_container:
        stego_container.write(''.join(container_data))

    if message_index == message_len:
        return True
    else:
        return False


def read_from_stegocontainer(stego_filename: str):
    with open(stego_filename, 'r', encoding='utf-8') as stegocontainer_file:
        stegofile_data = stegocontainer_file.read()

        return stegofile_data


def convert_binary_to_float(binary):
    _binary = binary
    val, i, n = 0, 0, 0
    while _binary != 0:
        dec = _binary % 10
        val = val + dec * pow(2, i)
        _binary = _binary // 10
        i += 1
    return val


def decode_message_from_stegocontainer(stego_filename: str):
    stegocontainer_data = read_from_stegocontainer(stego_filename)

    decoded_message = []
    scindx = 0
    for scindx in range(len(stegocontainer_data)):
        if stegocontainer_data[scindx] in FROM_RUSSIAN_TO_ENGLISH_LETTERS.values():
            decoded_message.append('1')
        elif stegocontainer_data[scindx] in FROM_RUSSIAN_TO_ENGLISH_LETTERS.keys():
            decoded_message.append('0')

    binary_message = ''.join(decoded_message).rstrip('0')
    print(f'binary message during decoding: {binary_message}')

    if len(binary_message) % 8 != 0:
        binary_message += (8 - (len(binary_message) % 8)) * '0'

    n = int('0b' + binary_message, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode('windows-1251', 'ignore') or '\0'


def main():
    # ok = encode_message_into_stegocontainer(
    #     'A я',
    #     'container.txt',
    #     'stegocontainer.txt',
    # )
    # print('message encoded')

    message = decode_message_from_stegocontainer('stegocontainer.txt')
    print(f'message decoded: {message}')


if __name__ == '__main__':
    main()