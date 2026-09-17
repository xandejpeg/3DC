"""Cortes femininos 2–12: reuse the delivered head, build only the hair.

Blender --factory-startup -b -t 2 --python-exit-code 1 --python
scripts/rcl-cabelos.py -- --cut 2 [--deliver]

Each cut is an independent checkpoint. Preview runs never publish a GLB.
The scalp envelope, parting, fall, fringe and curl rhythm are related controls;
they are not whole-head scaling. Source faces and facial modules stay untouched.
"""
import argparse, bpy, bmesh, math, json, random, sys, hashlib
from bisect import bisect_right
from pathlib import Path
from collections import Counter
from mathutils import Vector
from mathutils.bvhtree import BVHTree

R = Path(__file__).resolve().parents[1]
OUT = R / 'artifacts/cabelos-femininos-v1'
PUBLIC = R / 'public/models/rcl-feminino-v2'
args = argparse.ArgumentParser()
args.add_argument('--cut', type=int, required=True, choices=range(2, 13))
args.add_argument('--deliver', action='store_true')
args.add_argument('--views', action='store_true')
A = args.parse_args(sys.argv[sys.argv.index('--') + 1:])
CUT = A.cut
D = OUT / f'corte-{CUT:02d}'
D.mkdir(parents=True, exist_ok=True)
rng = random.Random(1709 + CUT)

# Read the existing scene as a library: no regenerated face, no historical QA scenes.
with bpy.data.libraries.load(str(R / 'artifacts/conjunto-feminino-v2/conjunto-feminino-v2.blend')) as (src, dst):
    dst.scenes = ['RCL_Faciais_01']
s = dst.scenes[0]
bpy.context.window.scene = s
for other in list(bpy.data.scenes):
    if other != s:
        bpy.data.scenes.remove(other)
s.name = f'RCL_Corte_Feminino_{CUT:02d}'
bases = sorted([o for o in s.objects if str(o.get('module_id', '')).startswith('base-f-') and not o.get('base_id')], key=lambda o: o['module_id'])
oldhair = next(o for o in s.objects if o.get('module_id') == 'hair-f-01')
root = oldhair.parent
bpy.data.objects.remove(oldhair, do_unlink=True)
fixed = {b['module_id']: [o for o in s.objects if o.get('base_id') == b['module_id']] for b in bases}
shared = [o for o in s.objects if str(o.get('module_id', '')).startswith(('eye-', 'nose'))]
bpy.context.view_layer.update()

def geo_hash(o):
    return hashlib.sha256(str(([tuple(v.co) for v in o.data.vertices], [tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest()
source_hashes = {o.name: geo_hash(o) for o in s.objects if o.type == 'MESH'}

# Profile is reused from the original source, without executing scene creation.
source = (R / 'artifacts/piloto-feminino-01/scripts/01_base.py').read_text(encoding='utf8')
exec(source[source.index('profiles=['):source.index('zs=sorted')])

def smooth(a, b, x):
    t = max(0, min(1, (x-a)/(b-a)))
    return t*t*(3-2*t)

SPECS = {
    2: dict(label='Longo em camadas com franja', end=.017, front=.252, volume=.008, part='crown', refs=['R053','R001','R005']),
    3: dict(label='Rabo lateral baixo com franja', end=.147, front=.253, volume=.002, part='swept', refs=['R054','R001','R005']),
    4: dict(label='Bob com franja reta', end=.085, front=.252, volume=.010, part='crown', refs=['R055','R002','R006']),
    5: dict(label='Dois rabos baixos', end=.153, front=.268, volume=.002, part='center', refs=['R056','R002','R006']),
    6: dict(label='Médio repartido ao centro', end=.034, front=.269, volume=.006, part='center', refs=['R057','R002','R006']),
    7: dict(label='Cacheado curto', end=.135, front=.249, volume=.012, part='curls', refs=['R058','R003','R007']),
    8: dict(label='Cachos em espiral', end=.025, front=.272, volume=.011, part='center', refs=['R059','R003','R007']),
    9: dict(label='Afro volumoso', end=.067, front=.248, volume=.044, part='curls', refs=['R060','R003','R007']),
    10: dict(label='Ondulado lateral raspado', end=.129, front=.269, volume=.002, part='side', refs=['R061','R004','R008']),
    11: dict(label='Curto com desenhos raspados', end=.145, front=.247, volume=.001, part='crop', refs=['R062','R004','R008']),
    12: dict(label='Longo ondulado ao centro', end=.004, front=.271, volume=.013, part='center', refs=['R063','R004','R008']),
}
cfg = SPECS[CUT]

def mat(name, color, rough=.78):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color, 1)
    p = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value = (*color, 1)
    p.inputs['Roughness'].default_value = rough
    return m

mats = [mat('RCL_Castanho_Base', (.105,.041,.017)),
        mat('RCL_Castanho_Luz', (.134,.055,.024)),
        mat('RCL_Castanho_Medio', (.117,.046,.019)),
        mat('RCL_Castanho_Sulco', (.066,.025,.011)),
        mat('RCL_Elastico', (.016,.012,.011), .9),
        mat('RCL_Raspado', (.092,.039,.020)),
        mat('RCL_Desenho_Couro', (.64,.29,.115))]
# Vertex colors provide a continuous shave gradient with no external textures.
if CUT in (10,11):
    p=next(n for n in mats[5].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value=(1,1,1,1)
    vertex_color=mats[5].node_tree.nodes.new('ShaderNodeVertexColor');vertex_color.layer_name='RCL_ShavedFade'
    mats[5].node_tree.links.new(vertex_color.outputs['Color'],p.inputs['Base Color'])
V, F, MI, SM, groups = [], [], [], [], {}

def face(ids, mi=0, smooth=True):
    F.append(tuple(ids)); MI.append(mi); SM.append(smooth)

def tube(name, points, radius, depth=None, tone=0, taper=True, sides=8, outward=None):
    """Closed elliptical lock with a transported frame; curved paths retain volume."""
    start = len(V)
    points = [Vector(p) for p in points]
    previous = None
    for k, p in enumerate(points):
        t = k/(len(points)-1)
        tangent = (points[min(k+1,len(points)-1)]-points[max(k-1,0)]).normalized()
        n = Vector(outward) if outward else Vector((p.x,p.y,(p.z-.19)*.5))
        n -= tangent*n.dot(tangent)
        if n.length < .001: n = Vector((0,-1,0)) - tangent*tangent.dot(Vector((0,-1,0)))
        n.normalize()
        if previous and n.dot(previous)<0: n = -n
        previous = n
        side = tangent.cross(n).normalized()
        w = radius(t) if callable(radius) else radius
        h = depth(t) if callable(depth) else (depth if depth is not None else w)
        tip_at=.72 if isinstance(taper,bool) else float(taper)
        shape = ((.52+.48*math.sin(math.pi*min(t/.85,1)/2)) * max(.025,(1-smooth(tip_at,1,t))**.65)) if taper else 1
        for j in range(sides):
            a = 2*math.pi*j/sides
            V.append(tuple(p+side*(w*shape*math.cos(a))+n*(h*shape*math.sin(a))))
    for k in range(len(points)-1):
        for j in range(sides):
            # Broad longitudinal planes: restrained material contrast, no zebra bands.
            mi = tone if tone >= 4 else ([tone, tone, 1, 2, tone, 3, 3, tone][j%8])
            a = start+k*sides+j; b = start+k*sides+(j+1)%sides
            face((a,b,b+sides,a+sides),mi)
    face(tuple(reversed(range(start,start+sides))), tone)
    face(range(len(V)-sides,len(V)),tone)
    groups[name] = list(range(start,len(V)))

def bezier(cs, count=24):
    a,b,c,d = map(Vector,cs)
    return [a*(1-t)**3+b*3*(1-t)**2*t+c*3*(1-t)*t*t+d*t**3 for t in [i/(count-1) for i in range(count)]]

def lock(name, cs, width=.030, depth=.008, tone=0, count=24):
    tube(name,bezier(cs,count),width/2,depth,tone)

def end_z(a):
    a = abs((a+math.pi)%(2*math.pi)-math.pi)
    front = cfg['front']
    if CUT in (3,5,10,11):
        # Keep the ears visible on tied and shaved styles.
        return front*(1-smooth(.25,1.25,a))+.207*smooth(.25,1.25,a)-(.207-cfg['end'])*smooth(1.8,2.55,a)
    if CUT == 7:
        return front*(1-smooth(.3,1.55,a))+.166*smooth(.3,1.55,a)-.031*smooth(1.8,2.8,a)
    hem=cfg['end']+.012+.004*math.cos(a*11)
    return front*(1-smooth(.22,1.22,a))+hem*smooth(.22,1.22,a)

def envelope(a, z, inset=0):
    # Above the temples all styles use the same original scalp profile.
    # Below it, width/back fall together so long hair clears ears and neck.
    if CUT in (7,9):
        center,rz,rx,ry=(.213,.111,.104,.112) if CUT==7 else (.200,.151,.144,.149)
        f=math.sqrt(max(.0001,1-((z-center)/rz)**2))
        return Vector(((rx*f-inset)*math.sin(a),-(ry*f-inset)*math.cos(a),z))
    h = min(.3049,max(0,z-.009))
    w,f,b,_ = profile(h)
    if CUT not in (3,5,10,11):
        t = smooth(cfg['end'],.245,z)
        blend=1-smooth(.207,.273,z)
        # Smooth crown-to-fall transition; an abrupt profile change makes a ridge.
        fallw=(.075 if CUT in (2,4,6) else .090)+.020*math.sin(math.pi*t*.65)
        fallb=.093+.012*t
        w=w*(1-blend)+fallw*blend
        b=b*(1-blend)+fallb*blend
        f=f*(1-blend)+.079*blend
    volume = cfg['volume']
    if CUT == 9:
        volume *= .6+.4*smooth(.07,.25,z)
    # Profile itself approaches zero at the pole; radial padding tapers there too.
    pad = (.007+volume)*min(1,max(0,(.322-z)/.02))
    c = math.cos(a)
    x = (w+pad-inset)*math.sin(a)
    y = -(f+pad-inset)*max(c,0)**.58 if c>=0 else (b+pad-inset)*(-c)**.86
    return Vector((x,y,z))

def cap():
    start=len(V); sides=96; rows=32
    top={7:.324,9:.351}.get(CUT,.319)
    for layer in range(2):
        for k in range(rows):
            t=(k+1)/rows
            for j in range(sides):
                a=2*math.pi*j/sides
                z=top+(end_z(a)-top)*t
                p=envelope(a,z,.004 if layer else 0)
                # Thin taper at the boundary of shaved hair, not a detached helmet rim.
                if CUT in (10,11):
                    headz=min(.3049,z-.002)
                    p=Vector(head_point(a,headz,False))
                    n=Vector((math.sin(a),-math.cos(a),.25)).normalized()
                    p+=n*(.0016 if layer else .0034)
                V.append(tuple(p))
        st=start+layer*rows*sides
        for k in range(rows-1):
            for j in range(sides):
                a=st+k*sides+j;b=st+k*sides+(j+1)%sides;c=b+sides;d=a+sides
                mi=0
                if CUT in (10,11):
                    angle=2*math.pi*(j+.5)/sides
                    z=sum(V[v][2] for v in (a,b,c,d))/4
                    mi=5
                face((a,b,c,d) if layer==0 else (d,c,b,a),mi)
        pole=len(V);V.append((0,.004,top+(.0 if layer==0 else -.004)))
        for j in range(sides):
            face((pole,st+j,st+(j+1)%sides) if layer==0 else (pole,st+(j+1)%sides,st+j),0)
    for j in range(sides):
        a=start+(rows-1)*sides+j;b=start+(rows-1)*sides+(j+1)%sides
        face((a,a+rows*sides,b+rows*sides,b),0)
    groups['CALOTA_E_CAIMENTO']=list(range(start,len(V)))

def curtain(cut):
    # Closed skin under these locks gives a solid rear silhouette from all views.
    n=25 if cut not in (8,12) else 23
    for j in range(n):
        a=.71+(2*math.pi-1.42)*j/(n-1)
        phase=.65*j
        pts=[]
        end=cfg['end']+(.010*math.sin(j*2.3) if cut!=4 else .003*math.cos(j))
        top=.311-.005*math.cos(j*1.7)
        for k in range(42):
            t=k/41;z=top+(end-top)*t
            p=envelope(a+.12*math.sin(math.pi*t),z)
            nrm=Vector((math.sin(a),-math.cos(a),.1)).normalized()
            p+=nrm*.003
            if cut==2:
                p+=nrm*(.003*math.sin(t*math.pi*4+phase)*smooth(.2,.55,t))
            elif cut in (8,12):
                amp=(.010 if cut==8 else .013)*smooth(.22,.52,t)
                freq=3.8 if cut==8 else 2.35
                p.x+=amp*math.sin(t*math.tau*freq+phase)
                p.y+=amp*.72*math.cos(t*math.tau*freq+phase)
            elif cut==6:
                p+=nrm*(.003*math.sin(t*math.pi*2+phase))
            pts.append(p)
        tube(f'CAIMENTO_{j:02d}',pts,.014 if cut!=8 else .012,.0075 if cut not in (8,12) else .010,j%3,taper=.87 if cut in (8,12) else True)
    if cut==2:
        # Shorter locks break the long outline into layers, as R053/R001 show.
        for layer,ending in enumerate((.145,.078)):
            for j in range(15):
                a=.72+(math.tau-1.44)*j/14
                pts=[]
                for k in range(20):
                    t=k/19;z=.282+(.0+ending-.282)*t
                    p=envelope(a+.10*t,z)+Vector((math.sin(a),-math.cos(a),0))*(.008+.005*t)
                    p.x+=math.sin(a)*.012*smooth(.7,1,t)
                    pts.append(p)
                tube(f'CAMADA_{layer}_{j:02d}',pts,.017,.008,j%3)

def bangs(straight=False):
    for j in range(11):
        u=(j-5)/5
        end=.223 if straight else .220+.007*math.sin(j*1.4)
        sway=0 if straight else .008*math.sin(j*.72)
        cs=[(u*.018,-.007,.321),(u*.068+sway,-.076,.322),(u*.083+sway,-.100,.270),(u*.071+.003*math.sin(j),-.095,end)]
        if straight:
            tube(f'FRANJA_{j:02d}',bezier(cs),lambda t:.0105*(.65+.35*math.sin(t*math.pi/2)),.006,j%3,taper=False)
        else:lock(f'FRANJA_{j:02d}',cs,.025,.0075,j%3)

def center_front(cut):
    # Root and tip positions define the face opening together with the cap edge.
    for sign in (-1,1):
        # Front sweeps cover the crown shell and lead into the longer face frame.
        for row in range(3):
            z=.282+row*.012
            lock(f'RISCA_FRONTAL_{sign}_{row}',[(sign*.002,-.080+row*.008,z),(sign*.030,-.103+row*.007,z+.023),(sign*.080,-.099+row*.008,z-.010),(sign*.101,-.047+row*.009,z-.065)],.028,.008,row%3)
        for j in range(4):
            rootp=(sign*(.004+.003*j),-.044+.026*j,.323-.003*j)
            finish=.072 if cut==6 else (.036 if cut==8 else .012)
            if cut==5:finish=.121+.014*j
            cs=[rootp,(sign*(.069+.010*j),-.103+.020*j,.329),(sign*(.090+.007*j),-.104+.027*j,.131),(sign*(.063+.016*j),-.071+.028*j,finish+.010*j)]
            pts=bezier(cs,48)
            if cut in (8,12):
                for k,p in enumerate(pts):
                    t=k/(len(pts)-1)
                    amp=(.010 if cut==8 else .013)*smooth(.2,.46,t)
                    freq=3.6 if cut==8 else 2.15
                    p.x+=sign*amp*math.sin(t*math.tau*freq+j*.55)
                    p.y+=amp*.6*math.cos(t*math.tau*freq+j*.55)
            tube(f'RISCA_E_MOLDURA_{sign}_{j}',pts,.017 if cut!=8 else .014,.009,j%3,taper=.87 if cut in (8,12) else True)

def swept_cap():
    for j in range(30):
        a=math.tau*j/30
        pts=[]
        for k in range(25):
            t=k/24
            aa=a+.38*math.sin(math.pi*t)*(1 if CUT==3 else (1 if a<math.pi else -1))
            z=.314+(end_z(a)-.314)*t
            p=envelope(aa,z)+Vector((math.sin(aa),-math.cos(aa),0))*.004
            pts.append(p)
        tube(f'PENTEADO_{j:02d}',pts,.016,.006,j%3)

def pony(sign):
    center=Vector((sign*.105,.038,.155))
    # Dark elastic is part of the hair GLB, not a new app slot.
    ring=[center+Vector((.020*math.cos(a),.018*math.sin(a),-.006*math.cos(a)*sign)) for a in [math.tau*i/32 for i in range(33)]]
    tube(f'ELASTICO_{sign}',ring,.005,.005,4,taper=False)
    for j in range(12):
        a=math.tau*j/12
        rootp=center+Vector((.010*math.cos(a),.010*math.sin(a),0))
        cs=[rootp,center+Vector((sign*.035+.026*math.cos(a),.019*math.sin(a),-.035)),center+Vector((sign*.035+.023*math.cos(a),.026*math.sin(a),-.090)),center+Vector((sign*(.014+.012*math.sin(j)),.015*math.sin(a),-.124+.012*math.cos(j*2.2)))]
        lock(f'RABO_{sign}_{j}',cs,.029,.010,j%3)

def curly_clump(name, center, normal, radius, tone=0, flat=False):
    n=normal.normalized()
    side=n.cross(Vector((0,0,1)))
    if side.length<.05:side=n.cross(Vector((0,1,0)))
    side.normalize();up=side.cross(n).normalized()
    # Rounded irregular clumps support a visible coil. The original references
    # show bulky curls, not a flat pattern of tiny loops on a cap.
    st=len(V);rings=6;sides=9
    for k in range(1,rings):
        phi=math.pi*k/rings
        for j in range(sides):
            a=math.tau*j/sides
            p=center+side*(radius*1.05*math.sin(phi)*math.cos(a))+up*(radius*.89*math.sin(phi)*math.sin(a))+n*(radius*(.55 if flat else .83)*math.cos(phi))
            V.append(tuple(p))
    for k in range(rings-2):
        for j in range(sides):
            a=st+k*sides+j;b=st+k*sides+(j+1)%sides
            face((a,b,b+sides,a+sides),tone)
    for sign,k in [(1,0),(-1,rings-2)]:
        pole=len(V);V.append(tuple(center+n*(radius*(.55 if flat else .83)*sign)))
        for j in range(sides):face((pole,st+k*sides+j,st+k*sides+(j+1)%sides),tone)
    pts=[]
    for k in range(18):
        t=k/17;a=t*math.tau*1.10
        rr=radius*(.72-.53*t)
        pts.append(center+side*math.cos(a)*rr+up*math.sin(a)*rr+n*(radius*(.56+.32*t)*(.7 if flat else 1)))
    tube(name,pts,radius*.28,radius*.24,tone,taper=True,sides=6,outward=n)
    groups[name]=list(range(st,len(V)))

def crop_curls(afro=False):
    # Staggered rings keep curl scale stable while changing the overall envelope.
    rows=13 if afro else 11
    for row in range(rows):
        t=(row+.6)/rows
        top=.350 if afro else .323
        n=max(8,round(8+34*math.sin(math.pi*t*.76)))
        for j in range(n):
            a=math.tau*(j+(row%2)*.48+rng.uniform(-.16,.16))/n
            low=end_z(a)
            z=top+(low-top)*t+rng.uniform(-.003,.003)
            p=envelope(a,z)
            normal=Vector((p.x,p.y,(z-.205)*1.1)).normalized()
            r=(.014 if afro else .0105)*rng.uniform(.8,1.22)
            p+=normal*(rng.uniform(.002,.007))
            curly_clump(f'CACHO_{row:02d}_{j:02d}',p,normal,r,j%3)

def shaved_styles():
    if CUT==10:
        # Right side in the image is shaved; all long waves fall to image left.
        for j in range(6):
            y=-.030+j*.019
            lock(f'VARREDURA_TOPO_{j}',[(.048,y,.301),(.017,y-.080,.355),(-.077,y-.073,.295),(-.111,y-.031,.215)],.035,.010,j%3,36)
        for j in range(17):
            y=-.083+j*.012
            pts=bezier([(.035+.005*math.sin(j),y*.5,.303+.004*math.sin(j)),(-.073,y-.045,.357),(-.147,y-.022,.147),(-.080-.025*math.sin(j*.8),y-.014,.024+.012*math.sin(j*2))],55)
            for k,p in enumerate(pts):
                t=k/54
                p.x+=.011*math.sin(t*math.tau*2.8+j*.48)*smooth(.25,.5,t)
                p.y+=.007*math.cos(t*math.tau*2.8+j*.48)*smooth(.25,.5,t)
            tube(f'ONDA_LATERAL_{j:02d}',pts,.016,.010,j%3,taper=.88)
        # Short occipital locks connect the long side to the cropped nape.
        for j in range(9):
            a=1.65+(math.pi-1.65)*j/8
            pts=[envelope(a,.305-(.17*k/24))+Vector((math.sin(a),-math.cos(a),0))*.004 for k in range(25)]
            tube(f'NUCA_CURTA_{j}',pts,.012,.005,j%3)
    else:
        for row in range(14):
            t=(row+.5)/14
            n=max(8,round(55*math.sin(t*1.5)))
            # Uniform angles leave an exposed stripe at the side of the broad
            # frontal scalp. Distribute clumps by actual arc length instead.
            ring=[];distance=[0.0]
            for sample in range(257):
                a=math.tau*sample/256
                z=.312-(.079+.009*max(0,-math.cos(a)))*t
                p=envelope(a,z);ring.append(p)
                if sample:distance.append(distance[-1]+(p-ring[-2]).length)
            for j in range(n):
                d=distance[-1]*(j+(row%2)*.45)/n
                k=min(255,max(0,bisect_right(distance,d)-1))
                f=(d-distance[k])/max(1e-8,distance[k+1]-distance[k])
                p=ring[k].lerp(ring[k+1],f)
                normal=Vector((p.x,p.y,(p.z-.2)*1.3)).normalized()
                curly_clump(f'TOPO_CRESPO_{row}_{j}',p+normal*.001,normal,.008*rng.uniform(.82,1.15),j%3,True)
        # Curving lines follow the scalp surface, so the design belongs to this module.
        paths=[[(.43,.218),(.72,.215),(1.00,.234),(1.18,.268)],
               [(.55,.208),(.95,.215),(1.14,.245),(1.24,.268)],
               [(.67,.216),(1.12,.218),(1.32,.255),(1.32,.266)],
               [(.75,.214),(1.25,.210),(1.48,.257),(1.62,.242)]]
        for j,cs in enumerate(paths):
            uv=bezier([(a,0,z) for a,z in cs],35)
            pts=[]
            for p in uv:
                q=Vector(head_point(p.x,p.z,False));q+=Vector((math.sin(p.x),-math.cos(p.x),.2)).normalized()*.0042
                pts.append(q)
            tube(f'DESENHO_CURVA_{j}',pts,.0013,.0007,6,taper=False)
        for j,(a,z) in enumerate([(.68,.247),(.93,.259),(1.15,.276)]):
            for diag in (-1,1):
                pts=[]
                for k in range(7):
                    t=k/6-.5;aa=a+t*.105;zz=z+diag*t*.009
                    p=Vector(head_point(aa,zz,False))+Vector((math.sin(aa),-math.cos(aa),.2)).normalized()*.0045
                    pts.append(p)
                tube(f'DESENHO_CRUZ_{j}_{diag}',pts,.0011,.0006,6,taper=False)

cap()
if CUT in (2,4,6,8,12):
    curtain(CUT)
    if CUT in (2,4):bangs(CUT==4)
    else:center_front(CUT)
elif CUT in (3,5):
    swept_cap()
    if CUT==3:
        bangs(False)
        for sign in (-1,1):
            for j in range(2):
                lock(f'MECHA_SOLTA_{sign}_{j}',[(sign*.030,-.052,.307),(sign*.090,-.098,.280),(sign*(.092+.008*j),-.078,.160),(sign*(.063+.025*j),-.064,.078+.027*j)],.024,.007,j)
        pony(1)
    else:
        center_front(5);pony(-1);pony(1)
elif CUT in (7,9):crop_curls(CUT==9)
else:shaved_styles()

mesh=bpy.data.meshes.new(f'CorteF{CUT:02d}_MechasEditaveis')
mesh.from_pydata(V,[],F);mesh.update()
bm=bmesh.new();bm.from_mesh(mesh)
bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
hair=bpy.data.objects.new(f'RCL_Corte_Feminino_{CUT:02d}',mesh)
s.collection.objects.link(hair);hair.parent=root
for m in mats:mesh.materials.append(m)
for p,mi,sm in zip(mesh.polygons,MI,SM):p.material_index=mi;p.use_smooth=sm
for name,ids in groups.items():
    vg=hair.vertex_groups.new(name=name);vg.add(ids,1,'REPLACE')
hair['module_id']=f'hair-f-{CUT:02d}'
hair['compatibility']='rcl-female-scalp-v1'
hair['revision']='hair-expansion-v1'
hair['reference_ids']=','.join(cfg['refs'])
hair['estimated_regions']='rear volume and interior; no individual calibrated rear/profile references'

def points(o):return [o.matrix_world@v.co for v in o.data.vertices]
def bvh(o):return BVHTree.FromPolygons(points(o),[p.vertices[:] for p in o.data.polygons])

# Only hair vertices may move during clearance correction. Nearest-surface tests
# include the widest face and fixed ears; the five face meshes are never edited.
adjusted=set()
if CUT in (5,6,7,8,10,12):
    # Curved face-framing locks cross the temples. Independent nearest-normal
    # projections fold their triangles around ears. A shared radial envelope
    # resolves the whole ring consistently without moving any facial landmark.
    union_v=[];union_f=[]
    for o in [*bases,*shared,*[o for fs in fixed.values() for o in fs]]:
        st=len(union_v);union_v.extend(points(o))
        union_f.extend([tuple(st+i for i in p.vertices) for p in o.data.polygons])
    union=BVHTree.FromPolygons(union_v,union_f)
    angles=192;step=.002;z0=-.02;rows=176
    radial=[]
    for k in range(rows):
        row=[];z=z0+k*step
        for j in range(angles):
            a=math.tau*j/angles;d=Vector((math.sin(a),-math.cos(a),0))
            hit=union.ray_cast(Vector((0,0,z))+d*.5,-d,.51)[0]
            row.append(max(0,hit.dot(d)) if hit is not None else 0)
        radial.append(row)
    for v in mesh.vertices:
        x,y,z=v.co;r=math.hypot(x,y)
        if r<.00001:continue
        a=math.atan2(x,-y)%math.tau;j=int(a/math.tau*angles);k=int((z-z0)/step)
        nearby=[radial[kk][jj%angles] for kk in (k-1,k,k+1,k+2) if 0<=kk<rows for jj in (j-1,j,j+1,j+2)]
        bound=max(nearby,default=0)
        margin=.0065 if CUT==12 else .0038
        if CUT==10 and v.index<96*32:margin=.0048
        if bound>.0001 and r<bound+margin:
            v.co.x*= (bound+margin)/r;v.co.y*=(bound+margin)/r;adjusted.add(v.index)
else:
    obstacles=[*bases,*[o for fs in fixed.values() for o in fs if 'ear' in str(o.get('module_id',''))]]
    trees=[(o,bvh(o)) for o in obstacles]
    for repeat in range(3):
        for v in mesh.vertices:
            for o,tree in trees:
                p,n,idx,dist=tree.find_nearest(v.co)
                if p is None:continue
                signed=(v.co-p).dot(n)
                if dist<.028 and signed<.0016:
                    v.co=p+n*.0022;adjusted.add(v.index)
mesh.update()
if CUT in (10,11):
    colors=mesh.color_attributes.new(name='RCL_ShavedFade',type='FLOAT_COLOR',domain='CORNER')
    for p in mesh.polygons:
        for li in p.loop_indices:
            v=mesh.vertices[mesh.loops[li].vertex_index].co
            if p.material_index==5:
                a=math.atan2(v.x,-v.y)%math.tau
                t=.15+.85*smooth(end_z(a)-.002,end_z(a)+.029,v.z)
                col=tuple(skin*(1-t)+hair*t for skin,hair in zip((.64,.29,.115),(.080,.031,.014)))
                colors.data[li].color=(*col,1)
            else:colors.data[li].color=(1,1,1,1)
bpy.context.view_layer.update()

def show_base(i):
    for j,b in enumerate(bases,1):
        for o in [b,*fixed[b['module_id']]]:
            o.hide_render=j!=i;o.hide_set(j!=i)
    for o in [hair,*shared]:o.hide_render=False;o.hide_set(False)

show_base(1)
s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=420;s.render.resolution_y=470;s.render.resolution_percentage=100
s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
s.eevee.taa_render_samples=24
s.camera.data.ortho_scale=.425 if CUT!=9 else .46
target=Vector((0,0,.168))
def render(view,pos):
    s.camera.location=pos;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler()
    s.render.filepath=str(D/f'{view}.png');bpy.ops.render.render(write_still=True)

report=dict(cut=CUT,label=cfg['label'],references=cfg['refs'],parameters=cfg,
            status='preview',vertices=len(V),polygons=len(F),editable_groups=len(groups),
            clearance_adjusted_vertices=len(adjusted),source_geometry_unchanged=all(geo_hash(bpy.data.objects[n])==h for n,h in source_hashes.items()))
assert report['source_geometry_unchanged']
# Save before rendering: Ctrl+C cannot discard the modeling checkpoint.
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'corte-feminino-{CUT:02d}.blend'),compress=True)
(D/'progresso.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
render('frente',(0,-.9,.168))
render('tres-quartos',(.53,-.8,.29))
if A.views or A.deliver:
    render('perfil',(.9,0,.168));render('costas',(0,.9,.168))
    for o in s.objects:
        if o.type=='MESH' and o!=hair:o.hide_render=True
    render('isolado',(.53,-.8,.29));show_base(1)

if A.deliver:
    # This is the Blender production export, not a change to the app exporter.
    for o in s.objects:o.select_set(False)
    hair.select_set(True);root.select_set(True);bpy.context.view_layer.objects.active=hair
    path=D/f'corte-feminino-{CUT:02d}.glb'
    bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,use_active_scene=True,export_extras=True,export_yup=True,export_materials='EXPORT',export_animations=False,export_cameras=False,export_lights=False)
    def signature(o):
        o.data.calc_loop_triangles();p=points(o)
        return Counter(tuple(sorted(tuple(round(n,6) for n in p[i]) for i in t.vertices)) for t in o.data.loop_triangles)
    def color_factor(socket):
        if not socket.is_linked:return tuple(socket.default_value)
        node=socket.links[0].from_node
        if node.type=='VERTEX_COLOR':return (1,1,1,1)
        if node.type=='MIX' and node.blend_type=='MULTIPLY':
            return tuple(a*b for a,b in zip(color_factor(node.inputs[6]),color_factor(node.inputs[7])))
        raise AssertionError('Unverified base-color graph: '+node.type)
    def material_signature(o):
        result=[]
        for m in o.data.materials:
            n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
            result.append(tuple(round(x,6) for x in (*color_factor(n.inputs['Base Color']),n.inputs['Roughness'].default_value)))
        return sorted(set(result))
    used=set(p.material_index for p in hair.data.polygons)
    expected_materials=[]
    for i in used:
        n=next(n for n in hair.data.materials[i].node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        expected_materials.append(tuple(round(x,6) for x in (*color_factor(n.inputs['Base Color']),n.inputs['Roughness'].default_value)))
    q=bpy.data.scenes.new('QA_REIMPORT');bpy.context.window.scene=q
    bpy.ops.import_scene.gltf(filepath=str(path),import_shading='NORMALS',merge_vertices=False)
    imported=next(o for o in q.objects if o.type=='MESH')
    bpy.context.view_layer.update()
    report['roundtrip_geometry_equal']=signature(hair)==signature(imported)
    report['roundtrip_materials_equal']=sorted(set(expected_materials))==material_signature(imported)
    if CUT in (10,11):
        def color_samples(o):
            attr=o.data.color_attributes.active_color;pp=points(o);result={}
            assert attr is not None
            for loop in o.data.loops:
                key=tuple(round(n,6) for n in pp[loop.vertex_index])
                color=tuple(attr.data[loop.index if attr.domain=='CORNER' else loop.vertex_index].color)
                result.setdefault(key,set()).add(color)
            return result
        before,after=color_samples(hair),color_samples(imported)
        assert before.keys()==after.keys()
        error=max(min(max(abs(a-b) for a,b in zip(c,d)) for d in after[key]) for key,colors in before.items() for c in colors)
        report['roundtrip_vertex_color_max_error']=error
        assert error<.005,'Vertex color mismatch exceeds 8-bit quantization tolerance'
    ht=bvh(imported)
    report['intersections']={b['module_id']:dict(base=len(ht.overlap(bvh(b))),fixed=sum(len(ht.overlap(bvh(o))) for o in fixed[b['module_id']]),eyes_nose=sum(len(ht.overlap(bvh(o))) for o in shared)) for b in bases}
    assert report['roundtrip_geometry_equal'] and report['roundtrip_materials_equal'],report
    # A failure is recorded and the GLB stays outside the app until repaired.
    report['status']='validated' if all(not any(v.values()) for v in report['intersections'].values()) else 'needs_clearance_fix'
    (D/'progresso.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf8')
    bpy.context.window.scene=s
    if report['status']=='validated':
        import shutil
        shutil.copy2(path,PUBLIC/path.name)
    print('DELIVERY',json.dumps(report),flush=True)
else:print('PREVIEW',json.dumps(report),flush=True)
