# uncrx
Extract crx into Chrome extension package source files.

## Poikilos fork
* You can extract existing files, such as to allow
  installing an unsigned extension from the resulting directory
  (via Extensions, Developer Mode, Load unpacked).
* You can extract crx files with format version 3

## Usage

```
python uncrx.py https://chrome.google.com/webstore/detail/style-capture/ndemhkhpinfhbgadphhjdcckjglphfmh
```
or
(if already downloaded)
```
python uncrx.py filename.crx
```

## Developer Notes
The crx format is a zip file preceded by a special header (see
<https://developer.chrome.com/extensions/crx.html>).
