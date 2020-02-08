# web-recent-dmenu
Here's an example of how you could use this with dmenu or rofi. 

in your bashrc:

```
alias web='firefox "$($HOME/<PATH TO THE SRIPT> | dmenu)" & disown'
```
