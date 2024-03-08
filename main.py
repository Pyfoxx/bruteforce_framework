import argparse
import os
import string
import time
from functools import wraps
from itertools import product
from pathlib import Path

global parser, base_dict
parser = argparse.ArgumentParser()
base_dict = Path('/usr/share/wordlists/rockyou.txt').resolve()

# Can't be bothered to much for comments, used jetbrains AI, seems okay for most part This script is used as the
# main module for bruteforce, and is used to call any hash methode with any bruteforce mode you need. The hash module
# need a function defined by `def hash(password):`

class Colors:
    """

    This class represents a collection of ANSI escape codes used for coloring text in the terminal.

    Attributes:
        HEADER (str): ANSI escape code for header color.
        OKBLUE (str): ANSI escape code for OK blue color.
        OKCYAN (str): ANSI escape code for OK cyan color.
        OKGREEN (str): ANSI escape code for OK green color.
        WARNING (str): ANSI escape code for warning color.
        FAIL (str): ANSI escape code for fail color.
        ENDC (str): ANSI escape code to reset color.
        BOLD (str): ANSI escape code for bold text.
        UNDERLINE (str): ANSI escape code for underlined text.

    Example:
        To print text in OK green color:
            print(Colors.OKGREEN + "This is some text in OK green color" + Colors.ENDC)

        To print bold and underlined text in header color:
            print(Colors.BOLD + Colors.UNDERLINE + Colors.HEADER + "This is some bold and underlined text in header color" + Colors.ENDC)

    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def timeit(func):
    """
    Measure the execution time of a function.

    :param func: The function to be measured.
    :return: A tuple containing the result of the function and the execution time in seconds.
    """
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        return (result,) + (total_time,)

    return timeit_wrapper


def arg_set():
    """
    setting up the argument.
    Called in the initialisation stack of the script
    :return: None
    """
    parser.add_argument('-T', "--type", help="The type of the hashes")
    parser.add_argument('-s', "--script_mode", help="type of target", choices=['single', 'file', 'hash_table'],
                        default='single')
    parser.add_argument('-b', '--hash', help="The hash to break")
    parser.add_argument('-d', "--dictionary", help="The dict that will be used", default=base_dict)
    parser.add_argument('-v', "--verbose", help="verbose", action='store_true')
    parser.add_argument('-f', "--file", help="treat a whole file of hashes")
    parser.add_argument('-a', "--attack_mode", help="Mode of attack", choices=['dict', 'brut'], default='dict')
    parser.add_argument('-m', "--min", help="least char for bruteforce", type=int, default=0)
    parser.add_argument('-M', "--max", help="Max amount of char", type=int, default=64)
    parser.add_argument('-ct', "--character_type", help="type to use ['alpha', 'numerical', 'special']",
                        choices=['alpha', 'numerical', 'special'], nargs='*', default=['alpha', 'numerical', 'special'])


def arg_parse():
    """
    Parses command line arguments
    Mainly here to set the hash module and early call errors in flags

    :return: None
    :raises FileNotFoundError: if the hash implementation file is not found
    :raises Exception: if a hash type, dictionary, or hash is not provided
    """
    global hash_module, flags
    flags = parser.parse_args()
    if flags.type:
        if os.path.exists(f'./hash/{flags.type}.py'):
            hash_module = __import__(f'hash.{flags.type}', fromlist=[flags.type])
        else:
            raise FileNotFoundError("import failed, file not found")
    else:
        raise Exception("please select a hash type")
    if not os.path.isfile(flags.dictionary):
        raise Exception("The dictionnary wasn't found")
    if not flags.hash and not flags.file:
        raise Exception("Please provide a hash")


@timeit
def dict_single_verbose():
    """
    Perform a verbose search in the dictionary file to find a line with a matching hash.

    :return: The line from the dictionary file if a matching hash is found, else False.
    """
    with open(flags.dictionary, 'r', encoding='ISO-8859-1') as d:
        for line in d:
            line = line.split('\n')[0]
            hash_line = hash_module.hash(line)
            print(f'{line} : {hash_line}')
            if hash_line == flags.hash:
                d.close()
                return line
        d.close()
        return False


@timeit
def dict_file_verbose(target):
    """
    :param target: Target hash value to search for in the dictionary file.
    :return: The line in the dictionary file that matches the target hash value. Returns `False` if no match is found.

    """
    with open(flags.dictionary, 'r', encoding='ISO-8859-1') as d:
        for line in d:
            line = line.split('\n')[0]
            hash_line = hash_module.hash(line)
            print(f'{line} : {hash_line}')
            if hash_line == target:
                d.close()
                return line
        d.close()
        return False



def dict_single():
    """
    :return: None
    """
    brute_result = dict_single_verbose()
    if not brute_result[0]:
        vprint(
            f"The hash `{Colors.FAIL}{flags.hash}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
    else:
        vprint(
            f"the hash : \'{Colors.FAIL}{flags.hash}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{brute_result[0]}{Colors.ENDC}\' in {Colors.OKBLUE}{brute_result[1]}{Colors.ENDC} seconds with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")


def dict_file():
    """
    Reads a file and performs a brute force algorithm on each target in the file.

    :return: None
    """
    with open(flags.file, 'r') as t:
        for target in t:
            target = target.split('\n')[0]
            brute_result = dict_file_verbose(target)
            if not brute_result[0]:
                vprint(
                    f"The hash `{Colors.FAIL}{flags.hash}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
            else:
                vprint(
                    f"the hash : \'{Colors.FAIL}{flags.hash}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{brute_result[0]}{Colors.ENDC}\' in {Colors.OKBLUE}{brute_result[1]}{Colors.ENDC} seconds with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
            t.close()


@timeit
def table_mode_verbose():
    """
    Constructs a hash table, reads passwords from a dictionary file, and checks if each password in the table matches with the target hash keys in a given file.

    :return: None
    """
    print("constructing table")
    hash_table = {}
    with open(flags.dictionary, 'r', encoding='ISO-8859-1') as d:
        for passwd in d:
            passwd = passwd.split('\n')[0]
            hashd = hash_module.hash(passwd)
            hash_table[hashd] = passwd
            print(hash_table[hashd])
        d.close()
    print("table successfully constructed, checking password now\n\n\n")
    hash_keys = list(hash_table.keys())
    with open(flags.file, 'r', encoding='ISO-8859-1') as t:
        for target in t:
            target = target.split('\n')[0]
            if target in hash_keys:
                vprint(
                    f"The hash : \'{Colors.FAIL}{target}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{hash_table[target]}{Colors.ENDC}\' with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
            else:
                vprint(
                    f"The hash : `{Colors.FAIL}{target}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
        t.close()



def table_mode():
    """
    Return the mode of the table.

    :return: None

    """
    print(table_mode_verbose())


def brut_single():
    """
    Perform a brute force attack on a single hash.

    :return: None
    """
    brute_result = brut_single_verbose()
    if not brute_result[0]:
        vprint(
            f"The hash `{Colors.FAIL}{flags.hash}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
    else:
        vprint(
            f"the hash : \'{Colors.FAIL}{flags.hash}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{brute_result[0][0]}{Colors.ENDC}\' in {Colors.OKBLUE}{brute_result[1]}{Colors.ENDC} seconds with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`, took `{Colors.OKCYAN}{brute_result[0][1]}{Colors.ENDC}` iterations")



@timeit
def brut_single_verbose():
    """
    Perform a brute force attack with verbose output.

    This method combines different character types (alpha, numerical, special) based on the flags.character_type input. It generates all possible combinations of characters and tests them
    * against a provided hash value (flags.hash).

    The method prints the characters being used for the attack, as well as each iteration of the loop and the generated test strings along with their respective hash values. If a match is
    * found, the method returns the matching test string and the total number of iterations. If no match is found, it returns False.

    @return: If a match is found, returns the matching test string and the number of iterations. If no match is found, returns False.
    """
    char = ''
    if 'alpha' in flags.character_type:
        print('adding alpha')
        char = char + string.ascii_letters
    if 'numerical' in flags.character_type:
        print('adding  numerical')
        char = char + string.digits
    if 'special' in flags.character_type:
        print('adding specials')
        char = char + string.punctuation
    print(f'will atack with:\n{char}')
    count = 0
    for i in range(flags.min, flags.max):
        print(f'loop #{i}')
        gen = product(char, repeat=i)
        for test in gen:
            count += 1
            test_hash = hash_module.hash(''.join(test))
            print(f'#{count} : {"".join(test)} : {test_hash}')
            if test_hash == flags.hash:
                return ''.join(test), count
    return False


@timeit
def brut_file_verbose(target, char):
    """
    .. function:: brut_file_verbose(target, char)

        This method performs a brute force attack on a file by generating all possible combinations of characters from the given character set. It compares the hash of each generated combination
    * with the target hash until a match is found or all combinations have been exhausted.

        :param target: The target hash to be matched.
        :type target: str
        :param char: The character set to be used for generating combinations.
        :type char: str
        :return: Returns a tuple containing the matching combination and the total number of combinations generated before finding the match. If no match is found, it returns False.
        :rtype: tuple or bool

        :Example:

        >>> target_hash = '5f4dcc3b5aa765d61d8327deb882cf99'
        >>> charset = 'abcdefghijklmnopqrstuvwxyz0123456789'
        >>> brut_file_verbose(target_hash, charset)
        ('password', 987654)

    """
    count = 0
    for i in range(flags.min, flags.max):
        gen = product(char, repeat=i)
        for test in gen:
            count += 1
            test_hash = hash_module.hash(''.join(test))
            print(f'{test} : {test_hash}')
            if test_hash == target:
                return ''.join(test), count
    return False


def brut_file():
    """
    Brute forces a file with specified characters.

    :return: None
    """
    with open(flags.file, 'r') as t:
        char = ''
        if 'alpha' in flags.character_type:
            print('adding alpha')
            char = char + string.ascii_letters
        if 'numerical' in flags.character_type:
            print('adding  numerical')
            char = char + string.digits
        if 'special' in flags.character_type:
            print('adding specials')
            char = char + string.punctuation
        print(f'will atack with:\n{char}')
        for target in t:
            target = target.split('\n')[0]
            brute_result = brut_file_verbose(target, char)
            if not brute_result[0]:
                vprint(
                    f"The hash `{Colors.FAIL}{flags.hash}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
            else:
                vprint(
                    f"the hash : \'{Colors.FAIL}{flags.hash}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{brute_result[0][0]}{Colors.ENDC}\' in {Colors.OKBLUE}{brute_result[1]}{Colors.ENDC} seconds with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`, took `{Colors.OKCYAN}{brute_result[0][1]}{Colors.ENDC}` iterations")
            t.close()


def func_selector():
    global vprint
    """
    Selects and executes the appropriate function based on the attack mode and script mode.

    :return: None
    """
    vprint = print
    if flags.verbose:
        def print(*args, **kwargs):
            pass
    match flags.attack_mode:
        case 'dict':
            match flags.script_mode:
                case None | 'single':
                    dict_single()
                case 'file':
                    dict_file()
                case 'hash_table':
                    if not flags.file:
                        raise Exception("This mode can only be used with a file")
                    else:
                        table_mode()
                case _:
                    print("please verify your atack type")
        case 'brut':
            match flags.script_mode:
                case None | 'single':
                    brut_single()
                case 'file':
                    brut_file()
                case _:
                    print("please verify your atack type")


if __name__ == "__main__":
    arg_set()
    arg_parse()
    func_selector()
