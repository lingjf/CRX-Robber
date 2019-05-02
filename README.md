# uncrx
Extract crx into Chrome extension package source files.

## Poikilos fork
* You can extract existing (already downloaded) files.
* You can extract crx version 3 files.

## Usage

* Download crx file
```
python uncrx.py filename.crx
```
* If the extension is on the chrome web store, this program is not
  needed. Install the extension using Chrome, and Chrome itself will
  extract the crx file to
  "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Extensions".

## Optional steps
Installing an unsigned extension from the resulting directory:
* Menu button, "More," "Extensions"
* Turn on Developer Mode.
* Click the "Load unpacked" button
* Choose the directory you extracted.

## Developer Notes
The crx format is a zip file preceded by a special header (see
<https://developer.chrome.com/extensions/crx.html>).

The Chrome web store doesn't seem to allow downloading anymore, or has
changed too much, so the following example fails:
```
python uncrx.py https://chrome.google.com/webstore/detail/style-capture/ndemhkhpinfhbgadphhjdcckjglphfmh
```

