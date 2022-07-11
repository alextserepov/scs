import json
import re

f=open('prov.json')
data = json.load(f)
for i in data:
    pre=re.sub('/nix/store/[0-9a-z]*-', '', i)
    post=re.sub('.drv', '', pre)
    post=re.sub('.tar.*', '', post)
    post=re.sub('.zip', '', post)
    post=re.sub('.tgz', '', post)
    if(re.search(r'\d', post) and not re.search('CVE', post, re.IGNORECASE) and not re.search('patch', post, re.IGNORECASE) and not re.search('\?', post) and not re.search('\.diff', post)):
        app = re.sub('-[0-9].*', '', post)
        ver = re.sub('.*-', '', post)
        if (len(app)>0 and len(ver)>0):
            print('{"app": "'+app+'", "version": "' + ver + '", "nix": "'+i+'"}')
f.close()
