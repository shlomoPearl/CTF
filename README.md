# CTF Writeups


A collection of my CTF writeups documenting solutions, tools used, and the reasoning behind each approach.

---

## OverTheWire

| Wargame | Category | Levels | Status | Writeup |
|---|---|---|---|---|
| [Bandit](https://overthewire.org/wargames/bandit/) | Linux CLI, networking, Git, cryptography | 0 → 33 | ✅ Complete | [View](./overthewire/bandit/README.md) |
| [Leviathan](https://overthewire.org/wargames/leviathan/leviathan0.html) | SUID binaries, ltrace, gdb, symlink attacks | 0 → 7 | ✅ Complete | [View](./overthewire/leviathan/README.md) |
| [Natas](./overthewire/natas/README.md) | Web security, HTTP, SQL injection, encoding | 0 → ? | 🔄 In progress | — |
| [Narnia](./overthewire/narnia/README.md) | Binary exploitation, buffer overflows | 0 → ? | ⏳ Upcoming | — |

---

## Skills Developed

### Linux & CLI
Comfortable navigating the Linux file system, writing bash scripts, managing permissions, working with processes, and chaining commands with pipes.

### Binary Analysis
Using `ltrace` to intercept library calls, `gdb` to disassemble and inspect binaries, identifying SUID privilege escalation vectors, and performing symlink attacks.

### Web Security *(in progress)*
HTTP fundamentals, cookies, source inspection, encoding schemes, basic injection techniques.

### Scripting
Python and bash for automating repetitive tasks — brute forcing, decoding, file manipulation.

---

## Repository Structure

```
ctf/
├── README.md                        ← you are here
└── overthewire/
    ├── bandit/
    │   └── README.md
    ├── leviathan/
    │   └── README.md
    ├── natas/
    │   └── README.md                ← in progress
    └── narnia/
        └── README.md                ← upcoming
```

---

## Tools & References

| Tool | Purpose |
|---|---|
| `ltrace` | Trace shared library calls in a binary |
| `gdb` | Disassemble, debug, and inspect compiled programs |
| `nc` / `openssl s_client` | Raw TCP / TLS connections |
| `find`, `grep`, `strings` | File system and content searching |
| `git log --all`, `git show` | Digging through repository history |
| `python`  | Quick decoding scripts (binary, hex, base64, etc.) |
