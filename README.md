from https://guyinatuxedo.github.io/

# Tools

## `objdump`

A section or function is seperated by an empty line. Hence changing the **FS** (Field Seperator) to newline and the **RS** (Record Seperator) to twice newline let you easily search for your recommended function, since it is simply to find within the `$1` field!
```bash
objdump -D name_of_your_obj_file -M intel | awk -F"\n" -v RS="\n\n" '$1 ~ /main/'
```
Of course you can replace `main` to any function you want to be output.


`rev50_linux64-bit` viens de [easy_reverse](https://crackmes.one/crackme/5b8a37a433c5d45fc286ad83)

## ghidra

Create a new project, add the binary, doubl-click on it, analyse it with default options + `Decompiler Parameter ID` (bc it improve the results)
Use the Bytes Windows with Ascii View enabled
Find main in the Symbols Tree 

Change the `main` function signature to `int main(int argc, char** argv)`.

Select a ligne and press `;` to put comments, Plate/Post/Pre and EOL comment are useful, they show on the Listing view, only the Pre comment appears on the Decompiler view.

You can rename variable to be more explicit.

Double click on a function to move to it.

Search for strings

Make bookmarks (for xor...)