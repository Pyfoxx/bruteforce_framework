def main(hash_module, target, flags, end, *args, **kwargs):
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
                end(hash_table[target])
            else:
                end(None)
        t.close()


if __name__ == "__main__":
    print("This tool should only be used as a module, if your seeing this, go back a folder and run the main script")