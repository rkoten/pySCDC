# pySCDC
S,C-dense coding in Python 3

### Usage
Put the text file (by default named `text.txt`) in the working directory of the script, run the script. It will create its vocabulary in `vocab.txt` as well as `encode` and `decode` folders.

Vocabulary consists of original text file's MD5 hashsum and text elements (words and punctuation) sorted by descending occurence popularity. By default supported punctuation is following: { `.,!?:;` }. You can change it by modifying `PATTERN` string at the top of the script.

Encode folder will contain 255 variants of dense codes (for each S parameter in `[1, 255]`).  
Decode folder will contain 255 copies of original text if worked correctly, each decoded from corresponding encode file.

### Script is pretty weakly tested, consider it an example implementation.

For theoretical information, refer to:

* (S,C)-Dense Coding: An Optimized Compression Code for Natural Language Text Databases (by Brisaboa, Fariña et al.; [link](https://www.dcc.uchile.cl/~gnavarro/ps/spire03.4.pdf)).
* On the Usefulness of Fibonacci Compression Codes (by Klein, Ben-Nissan; [link](https://pdfs.semanticscholar.org/62de/373af61cc71854f86028554a988f8a4dbe36.pdf)).
* http://vios.dc.fi.udc.es/codes/semistatic.html
