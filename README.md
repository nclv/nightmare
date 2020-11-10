Les sources du projet sont [ici](https://guyinatuxedo.github.io/).

# Rappels

Chaque caractère hexadécimal représente 4 bits.
2 caractères hexadécimaux représentent 8 bits ou 1 octet ou encore un byte.

Least Endian : `0xcaf3baee` devient `0xee 0xba 0xf3 0xca`

# Tools

## `objdump`

A section or function is seperated by an empty line. Hence changing the **FS** (Field Seperator) to newline and the **RS** (Record Seperator) to twice newline let you easily search for your recommended function, since it is simply to find within the `$1` field!
```bash
objdump -D name_of_your_obj_file -M intel | awk -F"\n" -v RS="\n\n" '$1 ~ /main/'
```
Of course you can replace `main` to any function you want to be output.


`rev50_linux64-bit` viens de [easy_reverse](https://crackmes.one/crackme/5b8a37a433c5d45fc286ad83)

## `ghidra`

Create a new project, add the binary, doubl-click on it, analyse it with default options + `Decompiler Parameter ID` (bc it improve the results)
Use the Bytes Windows with Ascii View enabled
Find main in the Symbols Tree 

Change the `main` function signature to `int main(int argc, char** argv)`.

Select a ligne and press `;` to put comments, Plate/Post/Pre and EOL comment are useful, they show on the Listing view, only the Pre comment appears on the Decompiler view.

You can rename variable to be more explicit.

Double click on a function to move to it.

Search for strings

Make bookmarks (for xor...)

## `gdb-gef`

If you are running a process in gdb, and wish to drop to the debugger console, you can do so by pressing `Ctrl-c`

To look at a function : `disas main`.

Now you can set a breakpoint. For instance if you want to set a breakpoint at the line `0x08048414 <+25>:    call   0x80482d0 <puts@plt>`, you write `b *main+25` or `b *0x08048414`.
You can set a breakpoint for function : `b *puts`

Use `info breakpoints` to show all breakpoints then `delete 2` to delete the second breakpoint

When we run the binary and it tries to execute that instruction, the process will pause and drop us into the debugger console.
It will show us the registers, stack and code.

For instance with the line `$esp   : 0xffffd010  →  0x080484b0  →  "hello world!"` we see that the register `esp` hold the value `0xffffd010` which is a pointer. With `x/g` you can see where it points as a *qword*, with `x/s` you can see where it points as a *string* and with `x/w` you can see where it points as a *dword*.

`info registers` will show all registers contents

`info frame` will show the stack frame

`p $register` then `set $register = value` to change the register contents

`x/g 0x402004` then `set *0x402004 = 0xfacade` to change the value stored at the memory address `0x402004` to `0xfacade`

`j *0x40117d` to jump directly to an instruction like `0x40117d`, and skip all instructions in between

`search-pattern pattern` to find a pattern in memory

## `pwntools`

See `pwn_usage_.py`

# CTF

Done :
- `stage-1.asm`
- `beleaf` : application d'une fonction sur chaque caractère de l'entrée, comparaison de sa sortie avec un byte d'un array `desiredOutput`, la fonction renvoie l'index du caractère dans l'array `lookup`. On prend à la suite les bytes de `desiredOutput` (qui doivent être égaux à l'index précedent pour constituder le bon mdp), puis on applique `(startaddresslookup + 4 * byte) = addresslookup` (l'adresse contenant la valeur du caractère recherché). Cela nous donne chaque caractère.
- `helithumper_re` : on check chaque caractère pour vérifier que c'est la bon avec un tableau dont les 4 premiers éléments sont initialisés (valeurs hexadécimales à convertir en ascii, fonction `chr` en python), la suite des éléments est initialisée manuellement dans des variables stockées à la suite du tableau dans le stack. On n'a pas d'erreur concernant l'indice auquel l'on souhaite accéder dans le tableau lorsque cet indice est plus grand que la taille du tableau. On itère alors sur la suite des valeurs du stack.
- `strings` : il suffit d'utiliser l'outils `strings`
- `boi` : 64 bit binary with a Stack Canary and Non-Executable stack, there is a `read()` function which will give us a way to overflow the stack with our own values. Regarder ce que contient le stack du main et calculer l'écart entre les addresses, on compare les valeurs 0xdeadbeef et 0xcaf3baee et on pop un shell si elles sont identiques. Passer à gdb pour observer la mémoire juste après l'appel au read (`b *0x4006a5`). 
  Use `search-pattern 15935728` with 15935728 our input. Then we saw `0x00007fffffffde20│+0x0010: "15935728\n"         ← $rsi` so with `x/10gx $rsi` we can see what contains the addresses after `0x00007fffffffde20` :
  ```
  0x7fffffffde20: 0x3832373533393531      0x000000000000000a
  0x7fffffffde30: 0xdeadbeef00000000      0x0000000000000000
  ```
  On compte le nombre de bytes à overflow : 16 + 4 (avec les 4 zéros devant `deadbeef`) ie. 0x14 bytes. So we give the input 00000000000000000000 + p32(0xcaf3baee). We need the hex address to be in **least endian** (least significant byte first) because that is how the elf will read in data, so we have to pack it that way in order for the binary to read it properly.
- `pwn1` : 32 bit binary with RELRO, a Non-Executable Stack, and PIE. You have to use the `gets` call to overwrite the contents of `local_18` to `0xdea110c8`. In order to reach the gets call, we will need to send the program the string "Sir Lancelot of Camelot\n" and "To seek the Holy Grail.\n". So we can see that `input` starts at offset `-0x43`. We see that `local_18` starts at offset `-0x18`. This gives us an offset of `0x43 - 0x18 = 0x2b` between the start of our input and `local_18`.
- `just_do_it` : 32 bit binary, with a non executable stack. So we can see that the string it is checking for is `P@SSW0RD`. Now since our input is being scanned in through an fgets call, a newline character `0x0a` will be appended to the end. So in order to pass the check we will need to put a null byte after `P@SSW0RD`. So we can see that `vulnBuf` can hold 16 bytes worth of data (0x28 - 0x18 = 16). However it appears that we can't reach the `eip` register to get RCE. However we can reach `target` which is printed with a puts call, right before the function returns. So we can print whatever we want. So we can see here that after it opens the flag.txt file, it scans in `0x30` ie. 48 bytes worth of data into `flag`. This is interesting because if we can find the address of `flag`, then we should be able to overwrite the value of `target` with that address and then it should print out the contents of `flag`, which should be the flag. That `flag` lives in the bss, with the address `0x0804a080`. There are 20 bytes worth of data between `vulnBuf` and `target` (`0x28 - 0x14 = 20`). So we can form a payload with 20 null bytes, followed by the address of flag.


Whenever you xor something by itself the result is 0.

## Binary analysis

`file binary`

`pwn checksec binary`

`strings binary | grep "char"`
