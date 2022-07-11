import json
import re

from cpe import CPE

# TODO: rewrite regexps in proper way, currently just quick hacks

f=open('prov.json')
data = json.load(f)
myj='{"entries": ['
for i in data:
    pre=re.sub('/nix/store/[0-9a-z]*-', '', i)
    post=re.sub('.drv', '', pre)
    post=re.sub('.tar.*', '', post)
    post=re.sub('.zip', '', post)
    post=re.sub('.tgz', '', post)
    if(re.search(r'\d', post) and not re.search('CVE', post, re.IGNORECASE) and not re.search('patch', post, re.IGNORECASE) and not re.search('\?', post) and not re.search('\.diff', post)):
        app = re.sub('-[0-9].*', '', post)


        app=re.sub('python3.9.','',app)
        app=re.sub('perl[0-9.]*','',app)
        app=re.sub('tcl[0-9.]*','',app)
        app=re.sub('_*','',app)
        app=re.sub('\.','',app)
        app=re.sub('\+','\+',app)


        ver = re.sub('.*-', '', post)
        ver = re.sub('\+[a-zA-z0-9]', '', ver)
        ver = re.sub('\.', '\.', ver)
        if (len(app)>0 and len(ver)>0):
            wfn='wfn:[part="a", product="'+re.sub('-', '\.', app)+'", version="'+ver+'", target_sw=ANY, target_hw=ANY]'
            c_wfn=CPE(wfn, CPE.VERSION_2_3)
            myj+='{"app": "'+app+'", "version": "' + ver + '", "nix": "'+i+'", "cpe": "'+c_wfn.as_fs()+'"}, '
myj=myj[:-2]+']'
print (myj)
f.close()
