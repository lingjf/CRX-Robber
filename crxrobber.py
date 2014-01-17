#!/usr/bin/env python
#-*coding:utf-8-*-'


import sys,os
import re
from sets import Set
import urllib2
import struct
import zipfile

def get_extension_ids(argv):
	ids = Set()
	for x in argv:
		m = re.search(r"([a-z]{32})", x)
		if m != None:
			for d in m.groups():
				ids.add(d)
	return ids			

def crx_download_url(extension_id):
	return "https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D" + extension_id + "%26uc"

def crx_file_name(extension_id):
	return extension_id + ".crx"	

def zip_file_name(extension_id):
	return extension_id + ".zip"	

def download_crx_file(extension_id):
	#os.system("wget '" + crx_download_url(extension_id) + "' --output-document " + crx_file_name(extension_id))	
	furl = urllib2.urlopen(crx_download_url(extension_id))
	with open(crx_file_name(extension_id),'wb') as fcrx:
		fcrx.write(furl.read())

def convey_crx_to_zip(extension_id):
	# https://developer.chrome.com/extensions/crx.html
	with open(crx_file_name(extension_id), 'rb') as fcrx:
		magic_number = fcrx.read(4)
		if magic_number != "Cr24":
			print "Corrupted crx file. Robber failed."
			sys.exit(0)

		version = fcrx.read(4)
		version, = struct.unpack("<I", version)
		
		public_key_length = fcrx.read(4)
		public_key_length, = struct.unpack("<I", public_key_length)
		
		signature_key_length = fcrx.read(4)
		signature_key_length, = struct.unpack("<I", signature_key_length)
		
		fcrx.seek(public_key_length + signature_key_length, os.SEEK_CUR)	
		with open(zip_file_name(extension_id), 'wb') as fzip:
			while 1:
				buf = fcrx.read(1)
				if not buf:
					break
				fzip.write(buf)

def extracts_zip_file(extension_id):
	zipfilename = zip_file_name(extension_id)
	unziptodir = extension_id

	if not os.path.exists(unziptodir): 
		os.mkdir(unziptodir, 0777)
	zfobj = zipfile.ZipFile(zipfilename)
	for name in zfobj.namelist():
		name = name.replace('\\','/')

		if name.endswith('/'):
			os.mkdir(os.path.join(unziptodir, name))
		else:           
			ext_filename = os.path.join(unziptodir, name)
			ext_dir= os.path.dirname(ext_filename)
			if not os.path.exists(ext_dir): 
				os.mkdir(ext_dir,0777)
			outfile = open(ext_filename, 'wb')
			outfile.write(zfobj.read(name))
			outfile.close()


def main(argv):
	extension_ids = get_extension_ids(argv)
	for extension_id in extension_ids:
		download_crx_file(extension_id)
		convey_crx_to_zip(extension_id)
		extracts_zip_file(extension_id)
		print 
		print extension_id + " captured."


if __name__ == "__main__":
	main(sys.argv[1:])

