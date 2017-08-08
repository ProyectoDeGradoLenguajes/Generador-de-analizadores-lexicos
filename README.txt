//   /$$     /$$  /$$$$$$  /$$$$$$$$ /$$$$$$$ 
//  |  $$   /$$/ /$$__  $$| $$_____/| $$__  $$
//   \  $$ /$$/ | $$  \ $$| $$      | $$  \ $$
//    \  $$$$/  | $$$$$$$$| $$$$$   | $$$$$$$/
//     \  $$/   | $$__  $$| $$__/   | $$____/ 
//      | $$    | $$  | $$| $$      | $$      
//      | $$    | $$  | $$| $$      | $$      
//      |__/    |__/  |__/|__/      |__/      


@Authors. "Idk why did we use @ but it feels kinda cool"
Joaquin Sanchez
Sebastian Pardo
Jorge Quinones

YAFP is a lexical analyzer generator oriented to manage
expressions in simple past, present and future inside
the project TLON in the National University of Colombia.

Use instructions:

1- Install python 3.5.0, you can do it from here https://www.python.org/downloads/release/python-350/.

install the requirements in the file requirements.txt, we recommend doing it with pip, just go to bash,
set it in the root of the actual project and exec:

pip install -r requirements.txt

If you dont have pip installed you can follow the documentation here:
https://pip.pypa.io/en/stable/installing/

2- YAFP recieves as input one file with 3 segmests with "(O_O¬)" indicator at the start of the line,
it should see something like that:

(O_O¬)  "imports"
<...Your code goes here...>
(O_O¬)  "Regular expressions"
<...Your code goes here...>
(O_O¬)  "other functions"
<...Your code goes here...>

Just fill it with python code, the imports and other functions segment is just python 3.5 code, the Regular expressions
segment have some rules that we will manage in the next section.
To compile your language just use:
python3 YAFP.py < input.txt

If everything goes well you should see a output.txt file in the directory of the proyect.

