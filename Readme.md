# Hash Brute Forcer

## Introduction
This project implements a versatile tool for brute-forcing hashes using various strategies. It supports dictionary-based attacks, single hash brute-forcing, and hash table mode for efficiently cracking multiple hashes. The script is designed to be flexible, allowing users to specify the type of hash, the attack mode, and other parameters for the brute force process.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributors](#contributors)
- [License](#license)

## Installation
No installation is necessary beyond cloning the repository and ensuring Python 3.x is installed on your system.

## Usage
The script is run from the command line, with various arguments controlling its operation:

Options include specifying the hash type, attack mode (dictionary, brute force, hash table), and other parameters such as the dictionary path or hash to crack.

## Features
- **Multiple Attack Modes**: Supports dictionary, brute force, and hash table attacks.
- **Flexible Hash Handling**: Can process single hashes, files containing multiple hashes, and supports a wide range of hash types.
- **Performance Metrics**: Measures and reports the time taken for operations, enhancing analysis and tuning.
- **Verbose Output**: Optional verbose output mode provides detailed operation logs.

## Dependencies
- Python 3.x
- argparse~=1.4.0
- Access to a dictionary file (e.g., `/usr/share/wordlists/rockyou.txt`) for dictionary attacks.
- If you want to use the hash table mode, a LOT of ram (think that python will need to store the hash and the word for every line of the dictionary)

## Configuration
Configuration is primarily through command-line arguments. See the [Usage](#usage) section for details on available options.

## Examples
To perform a dictionary attack on a single hash:

For more examples, refer to the [Usage](#usage) section.

## Troubleshooting
Ensure that the dictionary file path is correct and accessible. Verify that the specified hash type is supported.

## Contributors
To contribute to this project, please submit a pull request or open an issue for discussion.

## License
This project is open-sourced under the MIT License. See the LICENSE file for details.
