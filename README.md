# CTF Writeups


A collection of my CTF writeups documenting solutions, tools used, and the reasoning behind each approach.

---

## CTF Platforms

| Platform | Category | Levels | Status | Writeup |
|---|---|---|---|---|
| [PicoCTF - My Profile](https://learn.cylabacademy.org/users/shlomopearl) | Web/Binary exploitation, cryptography, forensics, reverse engineering | 135 challenges (80 easy, 55 medium) | 🔄 In progress | - |
| [WIZ Cloud Hunting](https://cloudhuntinggames.com/) | AWS, CloudTrail, malware analysis | 5 levels | ✅ Complete | [View](./WIZ/cloud-hunting-game/README.md) |
| [Bandit](https://overthewire.org/wargames/bandit/) | Linux CLI, networking, Git, cryptography | 0 → 33 | ✅ Complete | [View](./OTW/bandit/README.md) |
| [Leviathan](https://overthewire.org/wargames/leviathan/leviathan0.html) | SUID binaries, ltrace, gdb, symlink attacks | 0 → 7 | ✅ Complete | [View](./OTW/leviathan/README.md) |
| [Natas](https://overthewire.org/wargames/natas/) | Web security, HTTP, SQL injection, encoding | 0 → ? | 🔄 In progress | [view](./OTW/natas/README.md) |
| [Narnia](https://overthewire.org/wargames/narnia/) | Binary exploitation, buffer overflows | 0 → ? | ⏳ Upcoming | — |
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
├── README.md  
├── pico/
|   └── some solutions.py/sh scripts
├── WIZ/
|   └── cloud hunting game/ 
|       └── README.md                     
└── OTW/
    ├── bandit/
    │   └── README.md
    ├── leviathan/
    │   └── README.md
    ├── natas/
    │   └── README.md                
    └── narnia/
        └── README.md           
```

