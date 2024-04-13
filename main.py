import argparse
import os
import string
import time
from functools import wraps
from itertools import product
from pathlib import Path

# global parser, base_dict
parser = argparse.ArgumentParser()
base_dict = Path('/usr/share/wordlists/rockyou.txt').resolve()
logics_path = './logics/'
hash_path = './hash/'

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
    hash_choices = i = [x for x in os.listdir(f'{hash_path}') if os.path.isfile(f'{hash_path}{x}') and '.py' in x]
    hash_choices.pop(hash_choices.index("__init__.py"))
    parser.add_argument('-T', "--type", help="The type of the hashes", choices=hash_choices)
    atack_choices = i = [x for x in os.listdir(f'{logics_path}') if os.path.isfile(f'{logics_path}{x}') and '.py' in x]
    atack_choices.pop(atack_choices.index("__init__.py"))
    parser.add_argument('-a', "--attack_mode", help="Mode of attack", choices=atack_choices, default='dict')
    parser.add_argument('-b', '--hash', help="The hash to break")
    parser.add_argument('-S', "--slaves", help="in case of slaving")
    parser.add_argument('-s', "--script_mode", help="type of target", choices=['single', 'file', 'hash_table'],
                        default='single')
    parser.add_argument('-d', "--dictionary", help="The dict that will be used", default=base_dict)
    parser.add_argument('-v', "--verbose", help="verbose", action='store_true')
    parser.add_argument('-f', "--file", help="treat a whole file of hashes")
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
    # if flags.type:
    #     if os.path.exists(f'{hash_path}{flags.type}.py'):
    #         hash_module = __import__(f'hash.{flags.type}', fromlist=[flags.type])
    #     else:
    #         raise FileNotFoundError("import failed, file not found")
    # else:
    #     raise Exception("please select a hash type")
    if not os.path.isfile(flags.dictionary):
        raise Exception("The dictionnary wasn't found")
    if not flags.hash and not flags.file:
        raise Exception("Please provide a hash")


def end(*args, **kwargs):
    if len(args) == 1:
        return args[0]
    else:
        return args


def func_selector():
    """
    Selects and executes the appropriate function based on the attack mode and script mode.

    :return: None
    """
    if flags.slaves:
        slaves_list = flags.slaves.split(";")
        import flask
        # TODO : make slaves go brrrrrr
        # TODO : adjust logic so the slaves are ok
        # TODO : ask slaves first their power level so the work is distributed by it
    else:
        logic = __import__(f'logics.{flags.atack_mode}', fromlist=[flags.atack_mode])
        hash = __import__(f'hashs.{flags.hash}', fromlist=[flags.hash])
        # hash_module, target, flags, end, *args, **kwargs
        logic.main(hash_module=hash, target=flags.hash, flags=flags, end=end)





if __name__ == "__main__":
    arg_set()
    arg_parse()
    func_selector()
    # print(end('hello world'))
    # print(end('hello', 'world'))