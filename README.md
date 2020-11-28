# pySCDC
S,C-dense coding in Python 3

### Usage
Put the text file (by default named `text.txt`) in the working directory, run the script. It will create a vocabulary in `vocab.txt`, as well as `encode` and `decode` directories.

Vocabulary consists of source file's MD5 hashsum and text elements (words and punctuation) sorted by descending rate of occurrence. Default supported punctuation includes the following symbols: { `.,!?:;` }. It can be modified via `PATTERN` string defined at the top of the script.

Encode folder will contain 255 variants of dense codes (for each S value in `[1, 255]`).  
Decode folder will contain 255 copies of original text if worked correctly, each decoded from corresponding encode file.

*Script is weakly tested, consider it a sample implementation.*

### References
* (S,C)-Dense Coding: An Optimized Compression Code for Natural Language Text Databases (by Brisaboa, Fariña et al.; [link](http://web.archive.org/web/20201128053549/https://users.dcc.uchile.cl/~gnavarro/ps/spire03.4.pdf)).
* On the Usefulness of Fibonacci Compression Codes (by Klein, Ben-Nissan; [link](http://web.archive.org/web/20190225180907/http://pdfs.semanticscholar.org/62de/373af61cc71854f86028554a988f8a4dbe36.pdf)).
* [http://vios.dc.fi.udc.es/codes/semistatic.html (archive.org)](http://web.archive.org/web/20201128053727/http://vios.dc.fi.udc.es/codes/semistatic.html)
