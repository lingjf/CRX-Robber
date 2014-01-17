CRX-Robber
==========

Download Chrome extension package, and extract into source files.



1) Download crx files from chrome webstore

  There is no download button in chrome webstore. Althougth crx file is downloaded and saved to secret place, 
  it will be removed after installation. It is difficlut to fetch crx normally.
  
  http://productforums.google.com/forum/#!topic/chrome/g02KlhK12fU
  
2) Convey crx files to zip files

	In fact, crx is a zip file plus specific header. https://developer.chrome.com/extensions/crx.html.

	Removing specific header to convey crx to zip file.
	 
3) Extract zip files


Usage
==========

python crxrobber.py https://chrome.google.com/webstore/detail/style-capture/ndemhkhpinfhbgadphhjdcckjglphfmh
