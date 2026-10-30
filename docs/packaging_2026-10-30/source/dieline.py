# Dielines in millimetres -> SVG -> PDF/PNG
CUT='#E3001B'; FOLD='#0057B8'; BLEED='#00A651'; DIM='#333'
def svg(w,h,body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" font-family="Arial">{body}</svg>'
DASH='stroke-dasharray="3 2"'
def line(x1,y1,x2,y2,c,dash=False,w=.35): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" {DASH if dash else ""}/>'
def poly(pts,c,w=.35,fill='none'): return f'<polyline points="{" ".join(f"{x},{y}" for x,y in pts)}" stroke="{c}" stroke-width="{w}" fill="{fill}" stroke-linejoin="round"/>'
def text(x,y,t,s=3,c=DIM,a='middle',wt='normal'): return f'<text x="{x}" y="{y}" font-size="{s}" fill="{c}" text-anchor="{a}" font-weight="{wt}">{t}</text>'
def dimh(x1,x2,y,lab): return line(x1,y,x2,y,DIM,w=.2)+line(x1,y-1.5,x1,y+1.5,DIM,w=.2)+line(x2,y-1.5,x2,y+1.5,DIM,w=.2)+text((x1+x2)/2,y-1.2,lab,2.6)
def dimv(x,y1,y2,lab): return line(x,y1,x,y2,DIM,w=.2)+line(x-1.5,y1,x+1.5,y1,DIM,w=.2)+line(x-1.5,y2,x+1.5,y2,DIM,w=.2)+f'<text x="{x-1.2}" y="{(y1+y2)/2}" font-size="2.6" fill="{DIM}" text-anchor="middle" transform="rotate(-90 {x-1.2} {(y1+y2)/2})">{lab}</text>'

# ---------- CARTON: straight tuck end, inner 125 (L) x 105 (W) x 75 (H) ----------
L,W,H,G,T,D=125,105,75,15,20,50   # glue flap, tuck flap, dust flap depth
ox,oy=40,165                       # origin of body top-left (glue flap starts here)
xs=[ox, ox+G, ox+G+W, ox+G+W+L, ox+G+2*W+L, ox+G+2*W+2*L]  # glue|sideB|front|sideA|back
top,bot=oy,oy+H
b=''
# body folds (vertical)
for x in xs[1:-1]: b+=line(x,top,x,bot,FOLD,True)
# glue flap (tapered)
b+=poly([(xs[1],top),(xs[0],top+5),(xs[0],bot-5),(xs[1],bot)],CUT)
b+=f'<rect x="{xs[0]+1}" y="{top+6}" width="{G-2}" height="{H-12}" fill="#F2C94C" opacity=".35"/>'+text(xs[0]+G/2,top+H/2,'GLUE',2.4)
# right edge of back panel
b+=line(xs[5],top,xs[5],bot,CUT)
# TOP: closure panel on back panel (L x W) + tuck flap; dust flaps on sides
cx0,cx1=xs[4],xs[5]
b+=line(cx0,top,cx1,top,FOLD,True)
b+=line(cx0,top,cx0,top-W,CUT)+line(cx1,top,cx1,top-W,CUT)
b+=line(cx0,top-W,cx1,top-W,FOLD,True)
b+=poly([(cx0,top-W),(cx0+3,top-W-T+4),(cx0+8,top-W-T),(cx1-8,top-W-T),(cx1-3,top-W-T+4),(cx1,top-W)],CUT)
# window in top closure panel: inset 11 mm, r 4
wx,wy,ww,wh=cx0+11,top-W+11,L-22,W-22
b+=f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="4" stroke="{CUT}" stroke-width=".35" fill="#E6F2FF"/>'
b+=f'<rect x="{wx-5}" y="{wy-5}" width="{ww+10}" height="{wh+10}" rx="6" stroke="{BLEED}" stroke-width=".25" stroke-dasharray="1 1" fill="none"/>'
b+=text(wx+ww/2,wy+wh/2-2,'WINDOW',3.2,CUT,wt='bold')+text(wx+ww/2,wy+wh/2+3,f'{ww} x {wh} mm, R4',2.6)+text(wx+ww/2,wy+wh/2+7,'PET film 0.20 mm, overlap 5 mm (green)',2.4)
# top edges of front/sides/glue: dust flaps on sides, plain cut on front
for sx in (xs[1],xs[3]):
    b+=line(sx,top,sx+W,top,FOLD,True)
    b+=poly([(sx,top),(sx+2,top-D+12),(sx+14,top-D),(sx+W-3,top-D),(sx+W,top-6),(sx+W,top)],CUT)
b+=line(xs[2],top,xs[3],top,CUT)
b+=line(xs[0],top+5,xs[0],top+5,CUT)
# BOTTOM: closure panel on front panel + tuck; dust flaps on sides
fx0,fx1=xs[2],xs[3]
b+=line(fx0,bot,fx1,bot,FOLD,True)
b+=line(fx0,bot,fx0,bot+W,CUT)+line(fx1,bot,fx1,bot+W,CUT)
b+=line(fx0,bot+W,fx1,bot+W,FOLD,True)
b+=poly([(fx0,bot+W),(fx0+3,bot+W+T-4),(fx0+8,bot+W+T),(fx1-8,bot+W+T),(fx1-3,bot+W+T-4),(fx1,bot+W)],CUT)
for sx in (xs[1],xs[3]):
    b+=line(sx,bot,sx+W,bot,FOLD,True)
    b+=poly([(sx,bot),(sx+2,bot+D-12),(sx+14,bot+D),(sx+W-3,bot+D),(sx+W,bot+6),(sx+W,bot)],CUT)
b+=line(xs[4],bot,xs[5],bot,CUT)
# panel labels
labs=['SIDE B (QR)','FRONT','SIDE A','BACK (Supplement Facts)']
for i,lab in enumerate(labs):
    b+=text((xs[i+1]+xs[i+2])/2,top+H/2,lab,4,'#999',wt='bold')
b+=text((cx0+cx1)/2,top-W-T+9,'TUCK FLAP',2.6,'#999')+text((cx0+cx1)/2,top-W+8,'TOP PANEL',3,'#999',wt='bold')
b+=text((fx0+fx1)/2,bot+W/2,'BOTTOM PANEL (LOT / EXP)',4,'#999',wt='bold')
for sx in (xs[1],xs[3]): b+=text(sx+W/2,top-D/2,'DUST FLAP',2.6,'#999')+text(sx+W/2,bot+D/2,'DUST FLAP',2.6,'#999')
# dims
b+=dimh(xs[0],xs[1],bot+60,'15')+dimh(xs[1],xs[2],bot+60,'105')+dimh(xs[2],xs[3],bot+60+0,'')
b+=dimh(xs[3],xs[4],bot+60,'105')+dimh(xs[4],xs[5],bot+60,'125')+dimh(xs[2],xs[3],bot+W+T+8,'125')
b+=dimv(xs[5]+10,top,bot,'75')+dimv(xs[5]+10,top-W,top,'105')+dimv(xs[5]+10,top-W-T,top-W,'20')
b+=dimh(xs[0],xs[5],bot+W+T+22,f'overall {xs[5]-xs[0]} mm')+dimv(xs[0]-12,top-W-T,bot+W+T,f'overall {2*W+2*T+H} mm')
# legend + title
lx,ly=40,22
b+=text(lx,ly,'THE ALDERA · 30-Day Pass carton · straight tuck end (STE)',6,'#111','start','bold')
b+=text(lx,ly+8,'Inner size 125 (L) x 105 (W) x 75 (H) mm · holds 30 sachets standing in 2 rows of 15 · scale 1:1 on A2',3.4,'#333','start')
b+=text(lx,ly+14,'Board: 350 g/m² SBS (18 pt) · print CMYK + 1 Pantone (brand colour) · matte or soft-touch lamination · window with PET 0.20 mm',3.4,'#333','start')
b+=text(lx,ly+20,'Bleed 3 mm on all printed edges · safe area 3 mm inside folds · final dims to be confirmed by sample sachet with 2 capsules',3.4,'#333','start')
for i,(c,d,t) in enumerate([(CUT,False,'cut'),(FOLD,True,'fold / crease'),(BLEED,True,'bleed / film overlap')]):
    b+=line(lx+i*55,ly+30,lx+i*55+12,ly+30,c,d,.6)+text(lx+i*55+15,ly+31,t,3.2,'#333','start')
open('dieline_box.svg','w').write(svg(xs[5]+60,bot+W+T+40,f'<rect width="100%" height="100%" fill="#fff"/>'+b))

# ---------- SACHET: 50 x 70 mm, 3-side seal + top seal ----------
SW,SH=50,70; s=''
def sachet(x0,y0,title):
    o=''
    o+=f'<rect x="{x0}" y="{y0}" width="{SW}" height="{SH}" fill="#FBF7F0" stroke="{CUT}" stroke-width=".35"/>'
    # seals
    o+=f'<rect x="{x0}" y="{y0}" width="{SW}" height="8" fill="#000" opacity=".07"/>'
    o+=f'<rect x="{x0}" y="{y0+SH-5}" width="{SW}" height="5" fill="#000" opacity=".07"/>'
    o+=f'<rect x="{x0}" y="{y0}" width="5" height="{SH}" fill="#000" opacity=".07"/><rect x="{x0+SW-5}" y="{y0}" width="5" height="{SH}" fill="#000" opacity=".07"/>'
    # safe area
    o+=f'<rect x="{x0+8}" y="{y0+11}" width="{SW-16}" height="{SH-19}" fill="none" stroke="{BLEED}" stroke-width=".25" stroke-dasharray="1 1"/>'
    # tear notches
    ny=y0+12
    o+=poly([(x0,ny-1.5),(x0+3,ny),(x0,ny+1.5)],CUT)+poly([(x0+SW,ny-1.5),(x0+SW-3,ny),(x0+SW,ny+1.5)],CUT)
    o+=line(x0+3,ny,x0+SW-3,ny,DIM,True,.2)
    # capsules size 00: 23.3 x 8.5
    for cx in (x0+SW/2-6,x0+SW/2+6):
        o+=f'<rect x="{cx-4.25}" y="{y0+SH/2-11.65+4}" width="8.5" height="23.3" rx="4.25" fill="#fff" stroke="#999" stroke-width=".25"/>'
    o+=text(x0+SW/2,y0-4,title,3.6,'#111',wt='bold')
    return o
x0,y0=30,60
s+=sachet(x0,y0,'FRONT')+sachet(x0+80,y0,'BACK')
s+=dimh(x0,x0+SW,y0+SH+8,'50')+dimv(x0-7,y0,y0+SH,'70')
s+=dimv(x0+SW+6,y0,y0+8,'8')+dimh(x0,x0+5,y0+SH+15,'5')+dimv(x0+SW+6,y0+SH-5,y0+SH,'5')
s+=text(x0+SW+4,y0+12.8,'tear notch',2.4,CUT,'start')
s+=text(20,18,'THE ALDERA · Day Pass sachet · 3-side seal + top seal after filling',5,'#111','start','bold')
s+=text(20,26,'Finished size 50 x 70 mm · side and bottom seals 5 mm · top seal 8 mm · tear notches both sides 12 mm from top',3.2,'#333','start')
s+=text(20,32,'Laminate: matte OPP 20 / AL foil 7 / PE 50 µm (moisture barrier) · print both sides, up to 8 colours · contents: 2 capsules size 00',3.2,'#333','start')
s+=text(20,38,'Green dashed = safe area for text (3 mm inside seals) · grey = seal zones, no small text · LOT / EXP printed on the back by the line',3.2,'#333','start')
for i,(c,d,t) in enumerate([(CUT,False,'cut / outline'),(BLEED,True,'safe area'),(DIM,True,'tear line')]):
    s+=line(20+i*50,47,32+i*50,47,c,d,.6)+text(35+i*50,48,t,3,'#333','start')
open('dieline_sachet.svg','w').write(svg(250,150,f'<rect width="100%" height="100%" fill="#fff"/>'+s))
print('ok', xs[5]+60, bot+W+T+40)
