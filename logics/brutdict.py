def main(hash_module, target, flags, end, *args, **kwargs):
    """
    Perform a verbose search in the dictionary file to find a line with a matching hash.

    :return: The line from the dictionary file if a matching hash is found, else False.
    """
    with open(flags.dictionary, 'r', encoding='ISO-8859-1') as d:
        for line in d:
            line = line.split('\n')[0]
            hash_line = hash_module.hash(line)
            if hash_line == target:
                d.close()
                end(line)
        d.close()
        end(False)


if __name__ == "__main__":
    print("This tool should only be used as a module, if your seeing this, go back a folder and run the main script")