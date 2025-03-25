## Postavljanje VPS-a

1. Prvi login
`ssh root@ip-adresa`

2. Sad zelimo dodati korisnika u sudo grupu i onemoguciti ssh with root

```bash
adduser korisnik
usermod -aG sudo korisnik
```

3. Sad kad imamo korisnika u sudo grupi, mozemo onemoguciti ssh root.
   U file-u /etc/ssh/sshd_config postaviti `PermitRootLogin No` 

4. Mozemo resetirati ssh servis `sudo systemctl restart ssh`

### Postavljanje SSH putem privatnog i javnog kljuca
1. Generiraj par kljuceva velicine 4096 bitova

`ssh-keygen -b 4096` 

2. Kopirajmo javni kljuc i udjimo putem ssh u server

3. Zalijepimo kljuc u file .ssh/authorized_keys

4. Mozemo resetirati ssh servis `sudo systemctl restart ssh`

5. S ovog racunala sad se mozemo ulogirati bez koristenja lozinke 

### Postavljanje Django deploymenta

1. Postavljanje paketa
```bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt install nginx -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install git -y
```

2. Popratiti README.md upute


