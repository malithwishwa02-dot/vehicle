#!/usr/bin/env python3
import zipfile
import sys

def inspect(zip_path):
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        files = [n for n in names if not n.endswith('/')]
        print(f"Total entries: {len(names)}")
        sensitive = ['Local State','Default/History','Default/Login Data','Default/Preferences','Default/Web Data','Default/Cookies']
        for s in sensitive:
            found = [n for n in names if s in n]
            print(f"{s}: {len(found)} entries")
        # print a short sample
        print('\nSample Default entries:')
        for n in names:
            if n.startswith('37ab1612-c285-4314-b32a-6a06d35d6d84/Default/'):
                print(' -', n)
        
if __name__=='__main__':
    if len(sys.argv)<2:
        print('Usage: inspect_package.py <zipfile>')
        sys.exit(1)
    inspect(sys.argv[1])
