#!/usr/bin/env python

import sys
import os
import re
import struct
import zipfile

try:
    set
except NameError:
    from sets import Set as set
if sys.version_info.major >= 3:
    import urllib.request

    request = urllib.request
    from urllib.request import urlopen
else:
    import urllib2 as urllib

    request = urllib
    urlopen = urllib.urlopen

u = "https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D"


def get_extension_ids(argv):
    ids = set()
    for arg in argv:
        m = re.search(r"([a-z]{32})", arg)
        if m is not None:
            for d in m.groups():
                ids.add((d, None))
        elif "https://" not in arg:
            if os.path.isfile(arg):
                ids.add((None, arg))
            else:
                print("* '" + arg + "' does not exist.")
        else:
            print(
                "* '" + arg + "' is neither an 'Add to chrome' URL"
                " nor a local file path."
            )
    return ids


def crx_download_url(extension_id):
    return u + extension_id + "%26uc"


def crx_file_name(extension_id):
    return extension_id + ".crx"


def zip_file_name(name):
    return name + ".zip"


def download_crx(extension_id):
    # os.system("wget '" + crx_download_url(extension_id)
    #           + "' --output-document " + crx_file_name(extension_id))
    url_s = crx_download_url(extension_id)
    furl = urlopen(url_s)
    filename = crx_file_name(extension_id)
    print("* downloading '" + url_s + "'...")
    size = 0
    with open(filename, "wb") as crx_out:
        chunk = True
        while chunk:
            chunk = furl.read(1024)
            if len(chunk) < 1:
                break
            crx_out.write(chunk)
            size += len(chunk)
    if size < 1:
        filename = None
        print("  - The URL has nothing to read. The current")
        print("    chrome web store website is not supported.")
        print("    Download the file first.")
    else:
        print("  - downloaded " + str(size / 1024) + "KB")
    return filename


def name_to_id(filename):
    if filename[-4:].lower() == ".zip":
        filename = filename[:-4]
    if filename[-4:].lower() == ".crx":
        filename = filename[:-4]
    return filename.replace(".", "-")


def crx_to_zip(filename):
    # https://developer.chrome.com/extensions/crx.html
    ret = None
    # if filename is None:
    # filename = crx_file_name(extension_id)
    # if extension_id is None:
    # extension_id = name_to_id(filename)

    with open(filename, "rb") as crx_in:
        magic_number = crx_in.read(4)
        magic_number_s = None
        magic_number_s = magic_number.decode("utf-8")
        if magic_number_s != "Cr24":
            print("ERROR: '" + filename + "' is not a valid crx file.")
            print("  - magic number is " + magic_number_s)
            exit(1)

        version = crx_in.read(4)
        (version,) = struct.unpack(b"<I", version)

        print("  - version: " + str(version))

        public_key_length_s = crx_in.read(4)
        (public_key_length,) = struct.unpack(b"<I", public_key_length_s)
        print("  - public_key_length: " + str(public_key_length))
        zip_sig = b"\x50\x4b\x03\x04"

        if version <= 2:
            signature_key_length = crx_in.read(4)
            (signature_key_length,) = struct.unpack(b"<I", signature_key_length)
            print("  - signature_key_length: " + str(signature_key_length))
            if signature_key_length > 1024 * 4 / 8:
                print(
                    "    - WARNING: larger than normal"
                    " signature_key_length "
                    + str(signature_key_length)
                    + " ('"
                    + public_key_length_s.decode("utf-8")
                    + "')"
                )

            crx_in.seek(public_key_length + signature_key_length, os.SEEK_CUR)
        zip_name = zip_file_name(filename)
        wrote = 0
        if zip_name is None:
            print("  - can't generate zip name from " + str(filename))
        try:
            print("  - writing '%s'..." % zip_name)
            with open(zip_name, "wb") as fzip:
                buf = " "
                while buf:  # len(buf) > 0
                    buf = crx_in.read(1)
                    # print("    - '" + buf.decode('utf-8') + "'")
                    if buf:
                        ret = zip_name
                        fzip.write(buf)
                        wrote += 1
        except IOError as e:
            print("  - couldn't open or write to file (%s)." % zip_name)
        if ret is None:
            print("  - read 0 bytes from file (%s)." % filename)
        if wrote < 1:
            print("  - wrote 0 bytes to file (%s)." % zip_name)
    return ret


def extract_zip(zipfilename):
    unziptodir = name_to_id(zipfilename)
    if not os.path.exists(unziptodir):
        os.mkdir(unziptodir, 0o0777)

    zfobj = zipfile.ZipFile(zipfilename)
    for name in zfobj.namelist():
        name = name.replace("\\", "/")
        if name.endswith("/"):
            os.mkdir(os.path.join(unziptodir, name))
        else:
            ext_filename = os.path.join(unziptodir, name)
            ext_dir = os.path.dirname(ext_filename)
            if not os.path.exists(ext_dir):
                os.mkdir(ext_dir, 0o0777)
            outfile = open(ext_filename, "wb")
            outfile.write(zfobj.read(name))
            outfile.close()
    return unziptodir


def main(argv):
    extension_ids = get_extension_ids(argv)
    count = 0
    for extension_id, original_crx_name in extension_ids:
        crx_name = original_crx_name
        count += 1
        if crx_name is None:
            # Download
            print("* processing id '" + extension_id + "'...")
            crx_name = download_crx(extension_id)
            if crx_name is None:
                exit(2)
            print("  - captured '" + crx_name + "'")
        else:
            print("* processing file '" + crx_name + "'...")
        zip_name = crx_to_zip(crx_name)
        if zip_name is None:
            exit(3)
        print("  - converted to '" + zip_name + "'")
        unz_name = extract_zip(zip_name)
        if unz_name is None:
            exit(4)
        print("  - extracted to '" + unz_name + "'")
    if count < 1:
        print("")
        print("You must provide a local path to a crx file")
        # " or the full 'Add to chrome' URL starting with"
        # " https://.")
        print("")
        print("")


if __name__ == "__main__":
    main(sys.argv[1:])
