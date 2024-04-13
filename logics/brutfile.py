def main(flags, end, Colors):
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
                end(
                    f"The hash `{Colors.FAIL}{flags.hash}{Colors.ENDC}` cound not be broken with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`")
            else:
                end(
                    f"the hash : \'{Colors.FAIL}{flags.hash}{Colors.ENDC}\' has been matched to : \'{Colors.OKGREEN}{brute_result[0][0]}{Colors.ENDC}\' in {Colors.OKBLUE}{brute_result[1]}{Colors.ENDC} seconds with the algorythm being : `{Colors.OKCYAN}{flags.type}{Colors.ENDC}`, took `{Colors.OKCYAN}{brute_result[0][1]}{Colors.ENDC}` iterations")
            t.close()