#!/usr/bin/env python3
import os,re,sys,glob
D=sys.argv[1]; W=sys.argv[2] if len(sys.argv)>2 else ""
miss={}; n=0
for f in glob.glob(D+"/**/*.html",recursive=True):
    s=open(f,encoding="utf8",errors="ignore").read()
    for m in re.finditer(r'(?:href|src)="(/[^"#?]*)',s):
        u=m.group(1); n+=1
        cand=[D+u, D+u+"index.html", D+u.rstrip("/")+"/index.html"]
        if W: cand+= [W+u, W+u.rstrip("/")+"/index.html"]
        if not any(os.path.isfile(c) for c in cand): miss.setdefault(u,[]).append(f.replace(D,""))
print("links checked",n,"missing",len(miss))
for u,v in sorted(miss.items())[:40]: print(" ",u,"<-",v[:2])
