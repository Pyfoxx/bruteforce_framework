import string
from itertools import product
def brut_single_verbose(hash_module, target, flags, end, *args, **kwargs):
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
            if test_hash == target:
                end(''.join(test), count)
    end(False)


if __name__ == "__main__":
    print("This tool should only be used as a module, if your seeing this, go back a folder and run the main script")