# Vídeo do topo (mp4 + webm, desktop e celular) a partir das imagens das bolsas: zoom suave, fusões e cartão da marca.
import sys,subprocess,numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
GEN='/workspace/bolsas-src/gen/{}.jpg'
FONT='/usr/share/fonts/truetype/sand-box/google/Cormorant Garamond/CormorantGaramond-VariableFont_wght.ttf'
SCENES=[('20','Caramelo'),('17','Off-white'),('16','Preto'),('25','Rosa nude'),('21','Marrom'),('18','Off-white'),('23','Café'),('22','Caramelo')]   # (imagem 16:9, rótulo)
def sm(x): x=min(max(x,0),1); return x*x*(3-2*x)
def bbox(im):
    a=np.asarray(im,dtype=np.int16); border=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    bg=np.median(border,axis=0); m=np.abs(a-bg).max(axis=2)>34
    c=np.where(m.sum(axis=0)>12)[0]; r=np.where(m.sum(axis=1)>12)[0]; return c.min(),c.max(),r.min(),r.max()
def font(sz,w=600):
    f=ImageFont.truetype(FONT,sz)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f
def tracked(d,xy,t,f,fill,sp,anchor='l'):
    # texto com espaçamento entre letras
    w=sum(d.textlength(c,font=f)+sp for c in t)-sp; x,y=xy
    if anchor=='m': x-=w/2
    elif anchor=='r': x-=w
    for c in t: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+sp
def caption(im,label,mobile):
    im=im.copy(); d=ImageDraw.Draw(im); W,H=im.size; dark=(36,21,15); gold=(138,90,34)
    if mobile:
        tracked(d,(W/2,150),'MAISON CARAMELA · BOLSAS',font(26,600),gold,5,'m'); tracked(d,(W/2,186),label,font(56,500),dark,2,'m')
    else:
        tracked(d,(W-70,H-118),'MAISON CARAMELA · BOLSAS',font(22,600),gold,5,'r'); tracked(d,(W-70,H-92),label,font(54,500),dark,2,'r')
    return im
def desk_canvas(n):
    im=Image.open(GEN.format(n)).convert('RGB'); x0,x1,_,_=bbox(im); W,H=im.size
    # empurra a bolsa para a direita (texto fica à esquerda)
    shift=int(min(300,W*0.88-x1)); shift=max(shift,0)
    a=np.pad(np.asarray(im),((0,0),(shift,0),(0,0)),mode='edge')[:, :W]
    return Image.fromarray(a)
def mob_canvas(n,W=720,H=1280):
    im=Image.open(GEN.format(n)).convert('RGB'); x0,x1,y0,y1=bbox(im)
    side=int(max(x1-x0,y1-y0)*1.25); cx=(x0+x1)//2; cy=(y0+y1)//2
    a=np.asarray(im); l=cx-side//2; t=cy-side//2; w,h=im.size
    a=np.pad(a,((max(0,-t),max(0,t+side-h)),(max(0,-l),max(0,l+side-w)),(0,0)),mode='edge')
    sq=Image.fromarray(a[t+max(0,-t):t+max(0,-t)+side, l+max(0,-l):l+max(0,-l)+side]).resize((W,W),Image.LANCZOS)
    s=np.asarray(sq).astype(np.float32); top=s[:6].mean(axis=(0,1)); bot=s[-6:].mean(axis=(0,1))
    y=np.linspace(0,1,H)[:,None,None]; bg=top*(1-y)+bot*y; bg=np.broadcast_to(bg,(H,W,3)).copy()
    y0p=int(H*0.30)-W//2+60; fea=70
    m=np.ones((W,W,1),np.float32); ramp=np.linspace(0,1,fea)[:,None,None]
    m[:fea]*=ramp; m[-fea:]*=ramp[::-1]
    reg=bg[y0p:y0p+W]; bg[y0p:y0p+W]=reg*(1-m)+s*m
    return Image.fromarray(np.clip(bg,0,255).astype(np.uint8))
def card(W,H,mobile):
    im=Image.new('RGB',(W,H),(36,22,15)); a=np.asarray(im).astype(np.float32)
    yy,xx=np.mgrid[0:H,0:W]; cx,cy=(W*0.5,H*0.4) if mobile else (W*0.68,H*0.5)
    g=np.exp(-(((xx-cx)/(W*0.55))**2+((yy-cy)/(H*0.6))**2)); a+=g[...,None]*np.array([56,34,20])
    im=Image.fromarray(np.clip(a,0,255).astype(np.uint8)); d=ImageDraw.Draw(im)
    gold=(214,170,106); cream=(247,238,224)
    if mobile:
        tracked(d,(W/2,int(H*0.22)),'MAISON',font(100,500),cream,22,'m'); tracked(d,(W/2,int(H*0.22)+104),'CARAMELA',font(100,500),cream,10,'m')
        d.line((W/2-60,int(H*0.22)+290,W/2+60,int(H*0.22)+290),fill=gold,width=2)
        tracked(d,(W/2,int(H*0.22)+312),'BOLSAS',font(40,600),gold,18,'m')
    else:
        x=int(W*0.68); y=int(H*0.30)
        tracked(d,(x,y),'MAISON',font(112,500),cream,30,'m'); tracked(d,(x,y+104),'CARAMELA',font(112,500),cream,16,'m')
        d.line((x-60,y+250,x+60,y+250),fill=gold,width=2); tracked(d,(x,y+266),'BOLSAS',font(36,600),gold,20,'m')
    return im
def build(mobile):
    W,H=(720,1280) if mobile else (1280,720)
    L=[(mob_canvas(n) if mobile else desk_canvas(n)) for n,lab in SCENES]
    return W,H,L
def crop(im,z,dx,dy,W,H):
    sw,sh=im.size; cw=sw/z; ch=sh/z
    x0=(sw-cw)/2+dx*(sw-cw)/2; y0=(sh-ch)/2+dy*(sh-ch)/2
    return np.asarray(im.transform((W,H),Image.AFFINE,(cw/W,0,x0,0,ch/H,y0),resample=Image.BICUBIC),dtype=np.float32)
def frame(L,t,W,H,dur=3.4,ov=1.0,mobile=False):
    step=dur-ov; T=len(L)*step; t=t%T; acc=0; ws=0
    for i,im in enumerate(L):
        for off in (0,T,-T):
            u=t-i*step+off
            if 0<=u<=dur:
                w=sm(u/ov) if u<ov else (sm((dur-u)/ov) if u>dur-ov else 1)
                p=u/dur; z=(1.0+0.10*p) if i%2==0 else (1.10-0.10*p)
                acc=acc+w*crop(im,z,0.0,0.0,W,H); ws+=w
    return acc/max(ws,1e-6)
def run(out,mobile,fps=24):
    W,H,L=build(mobile); dur=len(L)*2.4
    cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(fps),'-i','-','-vf','eq=contrast=1.05:saturation=1.04,vignette=PI/6,format=yuv420p','-c:v','libx264','-preset','medium','-crf','24','-movflags','+faststart','-an',out+'.mp4']
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for f in range(int(dur*fps)): p.stdin.write(np.clip(frame(L,f/fps,W,H,mobile=mobile),0,255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg','-v','error','-y','-i',out+'.mp4','-c:v','libvpx-vp9','-b:v','0','-crf','38','-row-mt','1','-an',out+'.webm'])
    subprocess.run(['ffmpeg','-v','error','-y','-ss','3.6','-i',out+'.mp4','-frames:v','1','-vf','scale=iw:-2',out+'-poster.webp'])
if __name__=='__main__':
    run('video/hero-m',True) if sys.argv[1]=='m' else run('video/hero-d',False)
