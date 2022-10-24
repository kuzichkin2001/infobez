import os


def read_file_binaries(filename: str):
  with open(filename, 'rb') as file:
    file_contents = file.read()
    file_binary = bin(int(file_contents.hex(), 16))
    file_binary = file_binary.replace('0b', '')

    if len(file_binary) % 16 != 0:
      file_binary += (16 - len(file_binary)) * '0'

    hex_separated_parts = []
    for i in range(len(file_binary) // 16):
      hex_separated_parts.append(file_binary[16 * i:16 * (i + 1)])

    return hex_separated_parts


def walk_through_directory():
  current_dir = os.path.abspath('.')
  info_to_write = []
  for elem in os.walk(current_dir):
    path, directories, files = elem

    new_files = list(map(lambda x: f'{path}/{x}', files))
    for file in new_files:
      if not file.endswith('.fileinfo'):
        binaries = read_file_binaries(file)
        check_sum = count_check_sum(binaries)
        info_to_write.append((file, check_sum))

  return info_to_write


def count_check_sum(binaries: list[str]):
  check_sum = 0
  for binary in binaries:
    check_sum ^= int('0b' + binary, 2)

  return check_sum


def write_to_configuration_file(check_sums):
  with open('.fileinfo', 'w') as out_file:
    out_file.write('\n'.join([f'{filename}: {check_sum}' for filename, check_sum in check_sums]))


def read_configuration_file():
  with open('.fileinfo', 'r') as in_file:
    data = list(map(lambda x: x.rstrip('\n'), in_file.readlines()))

    check_sums_info = dict()
    for info_row in data:
      filename, check_sum = info_row.split(': ')

      check_sums_info[filename] = int(check_sum)

    return check_sums_info


def is_celostnost_ok():
  check_sums = read_configuration_file()
  current_info = walk_through_directory()

  for filename, check_sum in current_info:
    if filename not in check_sums.keys():
      print(f'{filename} was created with checksum {check_sum}')
    elif check_sums[filename] != check_sum:
      print(f'{filename} content has been changed.')

  write_to_configuration_file(current_info)


is_celostnost_ok()