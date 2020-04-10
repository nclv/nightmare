from pwn import *


# connect to the server at github.com (if you have an IP address, just swap out the dns name with the IP address) on port 9000 via tcp
target = remote("github.com", 9000)
# run a target binary
target = process("./challenge")
# attach the gdb debugger to a process
gdb.attach(target)
# attach the gdb debugger to a process, and also immediately pass a command to gdb to set a breakpoint at main
gdb.attach(target, gdbscript="b *main")

# Now for actual I/O. If we want to send the variable x to the target
# (target can be something like a process, or remote connection established by pwntools)
target.send(x)
# send the variable x followed by a newline character appended to the end
target.sendline(x)

# print a single line of text from target
print(target.recvline())
# print all text from target up to the string out
print(target.recvuntil("out"))

# ELFs store data via least endian, meaning that data is stored with the least significant byte first.
# In a few situations where we are scanning in an integer,
# we will need to take this into account. Luckily pwntools will take care of this for us.

# pack the integer x as a least endian QWORD (commonly used for x64)
p64(x)
# pack the integer x as a least endian DWORD (commonly used for x86)
p32(x)

# unpack a least endian QWORD and get it's integer value
u64(x)
# unpack a least endian DWORD and get it's integer value
u32(x)

# interact directly with target
target.interactive()