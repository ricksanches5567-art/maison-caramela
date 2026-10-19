# Recorta as imagens geradas (16:9) em quadrados 1:1 centralizados na bolsa e gera webp (img/p = grande, img/t = miniatura).
import numpy as np
from PIL import Image
SRC='/workspace/bolsas-src/gen/{}.jpg'
M={'BL-001':'20','BL-002':'16','BL-003':'26','BL-004':'21','BL-005':'07','BL-006':'22','BL-007':'14','BL-008':'25','BL-009':'23','BL-010':'17','BL-011':'18','BL-012':'24'}
def bbox(im):
    a=np.asarray(im.convert('RGB'),dtype=np.int16)
    border=np.concatenate([a[:8].reshape(-1,3),a[-8:].reshape(-1,3),a[:,:8].reshape(-1,3),a[:,-8:].reshape(-1,3)])
    bg=np.median(border,axis=0)
    d=np.abs(a-bg).max(axis=2)
    m=d>34
    cols=np.where(m.sum(axis=0)>12)[0]; rows=np.where(m.sum(axis=1)>12)[0]
    return cols.min(),cols.max(),rows.min(),rows.max()
for code,n in M.items():
    im=Image.open(SRC.format(n)).convert('RGB'); w,h=im.size
    x0,x1,y0,y1=bbox(im); cx=(x0+x1)//2
    cy=(y0+y1)//2; side=int(max(x1-x0,y1-y0)*1.22)
    left=cx-side//2; top=cy-side//2
    a=np.asarray(im)
    pl=max(0,-left); pr=max(0,left+side-w); pt=max(0,-top); pb=max(0,top+side-h)
    a=np.pad(a,((pt,pb),(pl,pr),(0,0)),mode='edge')
    a=a[top+pt:top+pt+side,left+pl:left+pl+side]
    sq=Image.fromarray(a)
    sq.save(f'/workspace/bolsas-src/sq/{code}.png')
    sq.resize((900,900),Image.LANCZOS).save(f'img/p/{code}.webp',quality=88,method=6)
    sq.resize((540,540),Image.LANCZOS).save(f'img/t/{code}.webp',quality=84,method=6)
    print(code,(x0,x1,y0,y1),'bag w',x1-x0,'left',left)
