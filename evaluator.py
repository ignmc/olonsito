import os
from os.path import join
from subprocess import Popen, PIPE

BINARY = 'interpreter.out'
TEST_FOLDER = 'testdata'


def write_file_input(input, user_id):
    input = input.strip()
    file_name = f'{user_id}-submission.sol'
    with open(file_name, 'w') as f:
        f.write(input)

    return file_name


def evaluate_case(answer_file, test_case):
    with open(join('testdata', f'{test_case}.in'), 'r') as testfile:

        evaluator = Popen([f'./{BINARY}', answer_file], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output = evaluator.communicate(testfile.read().encode())[0]

    return output


# def evaluate(answer_file):
#     output = {}
#     for filename in sorted(os.listdir(TEST_FOLDER)):
#         try:
#             output[filename] = evaluate_case(answer_file, filename).decode()
#         except Exception as e:
#             # jfc catch some decent exceptions
#             output[filename] = 'Ocurrió un error con tu código en este caso de prueba :c'
#
#     return output


def parse_result(result):
    if result.startswith(b'1'):
        return result.split(b'\n')[1].decode('utf-8')

    if result.startswith(b'2'):
        return "Olonso no recogió todos los objetos :c"

    if result.startswith(b'3'):
        return "Subtarea resuelta correctamente!"

    if result.startswith(b'4'):
        return "Tus instrucciones hicieron que Olonso entrara a un loop sin fin :c"

    return result.decode('utf-8')


def delete_file(file):
    os.remove(file)
