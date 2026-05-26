cut -c 23- server.log  | grep FLAGPART | uniq -u
exiftool
steghide --extract -sf img.jpg -p pAzzword