import sys, io, zipfile, urllib.request, os
URL=sys.argv[1]; OUT=sys.argv[2]; want=sys.argv[3:]
class RF(io.RawIOBase):
    def __init__(s,url):
        r=urllib.request.urlopen(urllib.request.Request(url,method='HEAD')); s.url=r.geturl(); s.size=int(r.headers['Content-Length']); s.pos=0
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s,o,w=0):
        s.pos = o if w==0 else s.pos+o if w==1 else s.size+o; return s.pos
    def read(s,n=-1):
        if n<0: n=s.size-s.pos
        if n==0 or s.pos>=s.size: return b''
        end=min(s.size,s.pos+n)-1
        req=urllib.request.Request(s.url,headers={'Range':f'bytes={s.pos}-{end}'})
        d=urllib.request.urlopen(req).read(); s.pos+=len(d); return d
    def readinto(s,b):
        d=s.read(len(b)); b[:len(d)]=d; return len(d)
f=io.BufferedReader(RF(URL),buffer_size=1<<20)
z=zipfile.ZipFile(f)
names=z.namelist()
if not want:
    for i in z.infolist(): print(i.filename,i.file_size); sys.exit()
os.makedirs(OUT,exist_ok=True)
for n in names:
    base=n.split('/')[-1]
    if base in want:
        with z.open(n) as src, open(os.path.join(OUT,base),'wb') as dst:
            while True:
                c=src.read(1<<20)
                if not c: break
                dst.write(c)
        print('got',n)
