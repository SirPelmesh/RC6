# Implementation of the RC6 encryption algorithm

## Installing

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.<br>
For this project, you will need Python 3.10 or higher, and maybe pandas and openpyxl libraries for avalanche effect.<br>
You can install the latest Python version from the official website, libraries can be installed using these commands:

```
pip install pandas
pip install openpyxl
```
There is also a requirements.txt.

## Description
The algorithm can work with three types of data:
<ol>
<li>string,</li>
<li>bytes,</li>
<li>bytearray.</li>
</ol>
Except key. key is always a string.

There are the following files:
<ul>
<li> random_data.py contains class RandomData which generates a string of particular length,</li>
<li> variables.py contains class Variables which stores constants and variables for RC6,</li>
<li> utils.py contains class Utils which contains the functions necessary for encryption and decryption,</li>
<li> rc6.py contains class RC6 that performs encryption / decryption using the RC6 algorithm,</li>
<li> and finally the main.py, where stored functions for testing the RC6 algorithm, calculation of the average avalanche effect and the main function for encryption and decryption. </li>
</ul>

This program was created for my course work, and it free to use :D
Good luck!
[SirPelmesh](https://github.com/SirPelmesh)
