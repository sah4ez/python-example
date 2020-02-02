#!/usr/bin/env python

from hashlib import md5

uniq = {}

with open('macs-hash', 'w') as hashes:
    with open('all.csv', 'r') as mac:
        for l in mac.read().splitlines():
            i = 0
            h = ""
            for x in l:
                h += x
                if i == 1:
                    h += " "
                    i = 0
                    continue
                i = 1
                
            h = h[:-1]
            try:
                bh = bytearray.fromhex(h)
                m = md5()
                m.update(bh)
                md5str = m.hexdigest()
                if md5str.lower() in uniq:
                    continue
                uniq[md5str.lower()] = ""
                hashes.write(md5str.upper()+",")
            except Exception as e:
                with open('errors', 'w') as w:
                    w.write("%s" % e)
                    w.write(l)
