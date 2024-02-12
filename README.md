<h1 align="center">OwO Selfbot</h1>
<img src="https://images-ext-2.discordapp.net/external/oEhS9a10eZMT_-nh6JgbgVE_9e7xk_2le8HHmlr1tZU/%3Fsize%3D4096/https/cdn.discordapp.com/avatars/408785106942164992/0cc7344c59b00ce1f4e5475c2e60b676.png?format=webp&quality=lossless&width=592&height=592" lt="poketwo autocatcher logo" align="left" height="80">

🐮 Donate for free using [Link1s](https://link1s.com/RealPhandat) and [Web1s](http://web1s.link/realPhandat)<br>
<a href="https://github.com/realphandat/OwO"><img src="https://hits.sh/github.com/realphandat/OwO.svg?view=today-total&label=Repo%20Today/Total%20Views&color=770ca1&labelColor=007ec6"/></a>
<a href="https://github.com/realphandat/OwO"><img src="https://img.shields.io/github/last-commit/realphandat/OwO" /></a><br>
[![Support Server](https://img.shields.io/badge/Support_Server-000?style=for-the-badge&logo=&color=informational)](https://discord.gg/DKbZu76QSD)
[![Stargazers](https://img.shields.io/github/stars/realphandat/OwO?style=for-the-badge&logo=&color=blue)](https://github.com/realphandat/OwO/stargazers)
[![Forks](https://img.shields.io/github/forks/realphandat/OwO?style=for-the-badge&logo=&color=blue)](https://github.com/realphandat/OwO/network/members)
[![Issues](https://img.shields.io/github/issues/realphandat/OwO?style=for-the-badge&logo=&color=informational)](https://github.com/realphandat/OwO/issues)


<h2 align="left">Features</h2>

* [x] Auto hunt, battle and Say owo/uwu </br>
* [x] Auto play gamble and Custom bet, rate </br>
* [x] Auto change spam channel (Custom) </br>
* [x] Auto claim daily </br>
* [x] Auto use gem </br>
* [x] Auto sleep </br>
* [x] Useful webhook logging </br>
* [x] Stop and Play music when Captcha appears </br>
* [ ] Auto solve Image/Link captcha </br>

<h2 align="left">Configurations</h2>

| Name  | Type | Description |
| ------------- | ------------- | ------------- |
| ```Token```  | ```String``` | Your account token |
| ```Nickname```  | ```String``` | Your display name. If you have a nickname in the spamming server, enter this instead of display name. If your name has more than 2 words, just enter 1 of the 2. For example, if your name is `Edogawa Conan`, just enter `Edogawa` or `Conan` |
| ```Channel```  | ```Array``` | The spam channel (You can add multi) |
| ```Prefix```  | ```String``` | The OwO's prefix in spamming server |
| ```OwO```  | ```Boolean``` | Customize owo/uwu command sending |
| ```Grind```  | ```Boolean``` | Customize hunt/battle command sending |
| ```Quote```  | ```Boolean``` | Customize quote sending (Get more exp) |
| ```Slot```  | ```Boolean``` | Customize slot playing |
| ```Sbet```  | ```Int``` | Customize slot start value |
| ```Srate```  | ```Int``` | Customize the multiplier when losing slot |
| ```Coinflip```  | ```Boolean``` | Customize coinflip playing |
| ```Cfbet```  | ```Int``` | Customize coinflip start value |
| ```Cfrate```  | ```Int``` | Customize the multiplier when losing coinflip |
| ```Daily```  | ```Boolean``` | Customize daily login |
| ```Gem```  | ```Boolean``` | Customize using gems (Worst to Best) |
| ```Sleep```  | ```Boolean``` | Custom sleep (Should enable to get less captchas) |
| ```Webhook```  | ```String``` | The Webhook's URL (Send important notifications) |

## Installation

### Window (PC & Laptop)
- Download and Install [Python](https://www.python.org/downloads)
- Download and Extract [OwO](https://github.com/realphandat/OwO/archive/refs/heads/main.zip)
- Open `install.bat`
- Open `setting.bat`
- Open `run.bat`

### Termux (Smartphone)
- Download and Install [Termux](https://f-droid.org/packages/com.termux)
- Open termux app and type:
```bash
pkg update
```
```bash
pkg upgrade
```
```bash
pkg install git
```
```bash
pkg install python
```
```bash
git clone https://github.com/realphandat/OwO.git
```
```bash
cd OwO
```
```bash
python -m pip install -r requirements.txt
```
```bash
python setting.py
```
```bash
python main.py
```
