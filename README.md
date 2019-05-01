# uncrx
Extract crx into Chrome extension package source files.
Extracting allows installing an unsigned crx file (via Extensions,
Developer Mode, )

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
