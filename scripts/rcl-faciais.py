"""Resume from the completed V1 scene: facial modules only, preview before export."""
import bpy,bmesh,math,json
from pathlib import Path
from collections import Counter,defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from mathutils.geometry import delaunay_2d_cdt
R=Path(__file__).resolve().parents[1];OUT=R/'artifacts/conjunto-feminino-v2'
OUT.mkdir(exist_ok=True);(OUT/'previas').mkdir(exist_ok=True)
s=bpy.data.scenes['RCL_Cinco_Bases_Cabelo_Unico'];bpy.context.window.scene=s;s.name='RCL_Faciais_01'
bases=sorted([o for o in s.objects if str(o.get('module_id','')).startswith('base-f-')],key=lambda o:o['module_id'])
hair=next(o for o in s.objects if o.get('module_id')=='hair-f-01');root=hair.parent
skin=bases[0].data.materials[0]
def material(name,color,rough=.8):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1)
    p=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
    p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
    return m
brown=material('RCL_Sobrancelha',(.075,.032,.015))
sclera=material('RCL_Esclera_01',(.88,.79,.64),.4)
iris=[material('RCL_Iris_01_'+str(i),c,.48) for i,c in enumerate([(.19,.065,.013),(.26,.10,.024),(.13,.038,.008),(.31,.13,.029)])]
pupil=material('RCL_Pupila',(.006,.003,.002),.3);shine=material('RCL_Reflexo',(.98,.97,.91),.2)
lip=material('RCL_Labio_Fixo',(.40,.135,.070));crease=material('RCL_Boca_Linha',(.105,.037,.019))
earshade=material('RCL_Orelha_Interior',(.44,.17,.071));nostril=material('RCL_Narina_Sombra',(.16,.047,.015))

def mesh(name,verts,faces,mat=skin,smooth=True,module=None,base=None):
    d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update()
    bm=bmesh.new();bm.from_mesh(d);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(d);bm.free()
    d.materials.append(mat)
    for p in d.polygons:p.use_smooth=smooth
    o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.parent=root
    if module:o['module_id']=module
    if base:o['base_id']=base
    o['revision']='rcl-facial-v2'
    return o
def facing(f,verts):
    a,b,c=[Vector(verts[i]) for i in f[:3]]
    return tuple(reversed(f)) if (b-a).cross(c-a).y>0 else tuple(f)
def surface(o):return BVHTree.FromPolygons([v.co for v in o.data.vertices],[p.vertices[:] for p in o.data.polygons])
def at(t,x,z):
    p=t.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))[0]
    assert p is not None,(x,z)
    return p.y
source=[v.co.copy() for v in bases[0].data.vertices]
polys=[p.vertices[:] for p in bases[0].data.polygons]
tree=surface(bases[0])
scalp_index=bases[0].vertex_groups['COURO_CABELUDO'].index
scalp_ids={v.index for v in bases[0].data.vertices if any(g.group==scalp_index for g in v.groups)}
orbital_repair={}
for i,p in enumerate(source):
    if p.y>=-.025 or i in scalp_ids:continue
    rr=min(math.sqrt(((p.x-a)/.0265)**2+((p.z-.177)/.025)**2) for a in [-.037,.037])
    if rr<1.6:
        t=max(0,min(1,(1.6-rr)/.45));t=t*t*(3-2*t)
        baseline=at(tree,0,p.z)+.028*(p.x/.075)**2
        orbital_repair[i]=t;p.y=p.y*(1-t)+baseline*t
# The former provisional recess is replaced by the actual lid interface.
tmp=bases[0].data.copy()
for v,p in zip(tmp.vertices,source):v.co=p
tmp.update();normals=[v.normal.copy() for v in tmp.vertices];bpy.data.meshes.remove(tmp)
specs=[('eye-L',-.037,.177,.0265,.025),('eye-R',.037,.177,.0265,.025),('nose',0,.146,.0145,.025)]
holes={};removed=set();neighbors=defaultdict(set)
for p in polys:
    for a,b in zip(p,(*p[1:],p[0])):neighbors[a].add(b);neighbors[b].add(a)
for key,cx,cz,rx,rz in specs:
    selected=[]
    for i,f in enumerate(polys):
        q=sum((source[j] for j in f),Vector())/len(f)
        if q.y<-.025 and ((q.x-cx)/rx)**2+((q.z-cz)/rz)**2<1:
            assert i not in removed,('overlapping interfaces',key)
            selected.append(i)
    edges=Counter(tuple(sorted((a,b))) for i in selected for a,b in zip(polys[i],(*polys[i][1:],polys[i][0])))
    adj=defaultdict(list)
    for (a,b),n in edges.items():
        if n==1:adj[a].append(b);adj[b].append(a)
    assert all(len(v)==2 for v in adj.values()),key
    start=next(iter(adj));loop=[start];prev=None;cur=start
    while True:
        nxt=next(n for n in adj[cur] if n!=prev)
        if nxt==start:break
        loop.append(nxt);prev,cur=cur,nxt
    assert len(loop)==len(adj),key
    holes[key]={'loop':loop,'spec':(cx,cz,rx,rz)};removed.update(selected)
# Only standardize interface vertices and a two-edge transition; preserve the scalp.
fixed=set(i for h in holes.values() for i in h['loop']);weight={i:1. for i in fixed}
ring=set(fixed)
for w in [.55,.18]:
    ring={j for i in ring for j in neighbors[i] if j not in weight}
    weight.update({i:w for i in ring})
for b in bases:
    print('CUT',b.name,flush=True)
    old=b.data;b.data=old.copy()
    for i,t in orbital_repair.items():
        v=b.data.vertices[i];v.co.y=v.co.y*(1-t)+source[i].y*t
    protected=next(g.index for g in b.vertex_groups if g.name=='COURO_CABELUDO')
    for i,w in weight.items():
        v=b.data.vertices[i]
        if any(g.group==protected for g in v.groups):
            assert (v.co-source[i]).length<1e-7,('scalp differs at interface',i)
            continue
        v.co=v.co.lerp(source[i],w)
    # Delete faces, retaining stable source indices and all meaningful vertex groups.
    bm=bmesh.new();bm.from_mesh(b.data);bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[bm.faces[i] for i in sorted(removed)],context='FACES_ONLY')
    bm.to_mesh(b.data);bm.free();b.data.update()
    print('CUT_DONE',b.name,flush=True)
    b['compatibility']='rcl-female-face-v2';b['revision']='rcl-set-v2'

def lid_y(cx,x,z):
    baseline=at(tree,0,z)+.028*(x/.075)**2
    d2=(x-cx)**2+(z-.177)**2
    if d2>=.022**2:return baseline
    sphere=-.060-math.sqrt(.022**2-d2)-.0012
    return .5*(baseline+sphere-math.sqrt((baseline-sphere)**2+.0015**2))
def patch(key,inner=None):
    h=holes[key];cx,cz,rx,rz=h['spec'];loop=h['loop'];N=len(loop)
    verts=[tuple(source[i]) for i in loop];faces=[]
    if inner:
        outer=[Vector((source[i].x,source[i].z)) for i in loop]
        aperture=[inner(2*math.pi*j/64) for j in range(64)]
        inside=[Vector((p.x,p.z)) for p in aperture]
        def contains(p,poly):
            yes=False
            for a,b in zip(poly,poly[1:]+poly[:1]):
                if (a.y>p.y)!=(b.y>p.y) and p.x<(b.x-a.x)*(p.y-a.y)/(b.y-a.y)+a.x:yes=not yes
            return yes
        coords=outer+inside
        edges=[(j,(j+1)%N) for j in range(N)]+[(N+j,N+(j+1)%64) for j in range(64)]
        for ix in range(-15,16):
            for iz in range(-14,15):
                p=Vector((cx+ix*.002,cz+iz*.002))
                if contains(p,outer) and not contains(p,inside):coords.append(p)
        vs,es,fs,orig,_,_=delaunay_2d_cdt(coords,edges,[],0,1e-8,True)
        verts=[];outermap={}
        for j,p in enumerate(vs):
            border=next((k for k in orig[j] if k<N),None)
            if border is not None:
                verts.append(tuple(source[loop[border]]));outermap[j]=loop[border]
            else:verts.append((p.x,lid_y(cx,p.x,p.y),p.y))
        for f in fs:
            c=sum((vs[i] for i in f),Vector((0,0)))/len(f)
            if contains(c,outer) and not contains(c,inside):faces.append(facing(f,verts))
    else:
        for r in [.78,.56,.34,.15]:
            for i in loop:
                p=source[i];x=cx+(p.x-cx)*r;z=cz+(p.z-cz)*r
                verts.append((x,nose_y(x,z),z))
        for k in range(4):
            for j in range(N):
                a=k*N+j;b=k*N+(j+1)%N;c=b+N;d=a+N
                faces.extend([facing((a,b,c),verts),facing((a,c,d),verts)])
        verts.append((cx,nose_y(cx,cz),cz));center=len(verts)-1
        for j in range(N):faces.append(facing((4*N+j,4*N+(j+1)%N,center),verts))
    obj=mesh('RCL_'+key+'_Pele',verts,faces,module=key+'-skin')
    # Match the shading to the untouched base at the module boundary.
    custom=[v.normal.copy() for v in obj.data.vertices]
    if inner:
        for j,v in enumerate(obj.data.vertices):
            x,y,z=v.co;eps=.00005
            custom[j]=Vector(((lid_y(cx,x+eps,z)-lid_y(cx,x-eps,z))/(2*eps),-1,(lid_y(cx,x,z+eps)-lid_y(cx,x,z-eps))/(2*eps))).normalized()
    for j,i in (outermap.items() if inner else enumerate(loop)):custom[j]=normals[i]
    obj.data.normals_split_custom_set_from_vertices(custom)
    obj['interface']=key
    return obj

eyes=[]
def globe(cx):
    # Static spherical eye segment: visible sclera ends inside the lid margin.
    # Hidden sphere caps are omitted; blinking/rotation is outside this static set.
    verts=[(cx,-.082,.177)];faces=[];N=48;M=8
    for j in range(1,M+1):
        for i in range(N):
            th=2*math.pi*i/N;r=j/M
            dx=.0205*math.cos(th)*r;dz=(.003 if math.sin(th)>=0 else .0135)*math.sin(th)*r
            verts.append((cx+dx,-.060-math.sqrt(.022**2-dx*dx-dz*dz),.177+dz))
    for i in range(N):faces.append(facing((0,1+i,1+(i+1)%N),verts))
    for j in range(M-1):
        for i in range(N):
            a=1+j*N+i;b=1+j*N+(i+1)%N
            faces.append(facing((a,b,b+N,a+N),verts))
    back=len(verts);verts.append((cx,-.035,.177))
    for i in range(N):faces.append((back,1+(M-1)*N+i,1+(M-1)*N+(i+1)%N))
    return mesh('RCL_Globo_'+str(cx),verts,faces,sclera,True,'eye-'+str(cx)+'-globe')
def disc(name,cx,cz,rx,rz,yfunc,mat,module,N=24):
    if module.startswith('nose-'):
        verts=[(cx,yfunc(cx,cz),cz)]+[(cx+rx*math.cos(2*math.pi*i/N),yfunc(cx+rx*math.cos(2*math.pi*i/N),cz+rz*math.sin(2*math.pi*i/N)),cz+rz*math.sin(2*math.pi*i/N)) for i in range(N)]
        return mesh(name,verts,[facing((0,1+i,1+(i+1)%N),verts) for i in range(N)],mat,True,module)
    verts=[(cx,yfunc(cx,cz),cz)];faces=[]
    for r in [.2,.4,.6,.8,1]:
        for i in range(N):
            th=2*math.pi*i/N;x=cx+rx*r*math.cos(th);z=cz+rz*r*math.sin(th)
            verts.append((x,yfunc(x,z),z))
    for i in range(N):faces.append(facing((0,1+i,1+(i+1)%N),verts))
    for k in range(4):
        for i in range(N):
            a=1+k*N+i;b=1+k*N+(i+1)%N
            faces.append(facing((a,b,b+N,a+N),verts))
    obj=mesh(name,verts,faces,mat,True,module)
    spherecx=-.037 if module.startswith('eye-L') else .037
    obj.data.normals_split_custom_set_from_vertices([(Vector(p)-Vector((spherecx,-.060,.177))).normalized() for p in verts])
    return obj
for key,cx,cz,rx,rz in specs[:2]:
    print('EYE',key,flush=True)
    def aperture(th,cx=cx):
        dx=.0205*math.cos(th);dz=(.003 if math.sin(th)>=0 else .0135)*math.sin(th)
        return Vector((cx+dx,-.060-math.sqrt(.022**2-dx*dx-dz*dz)-.0012,.177+dz))
    eyes.append(patch(key,aperture));eyes.append(globe(cx))
    def iris_y(x,z,cx=cx):return -.060-math.sqrt(max(.000001,.022**2-(x-cx)**2-(z-.177)**2))-.00020
    ir=disc('RCL_Iris_Castanha_'+key,cx,.178,.0105,.0105,iris_y,iris[0],key+'-iris')
    for m in iris[1:]:ir.data.materials.append(m)
    for p in ir.data.polygons:p.material_index=(p.index*7)%4
    eyes.append(ir)
    eyes.append(disc('RCL_Pupila_'+key,cx,.178,.0052,.0052,lambda x,z:iris_y(x,z)-.00015,pupil,key+'-pupil'))
    eyes.append(disc('RCL_Brilho_'+key,cx-.0028,.180,.0015,.0015,lambda x,z:iris_y(x,z)-.00035,shine,key+'-highlight',12))
    # Thin upper lid margin, tapered at both corners (the reference's outer contour).
    v=[]
    for i in range(25):
        x=cx-.0205+.041*i/24;dx=x-cx;z=.177+.003*math.sqrt(max(0,1-(dx/.0205)**2))
        for dz in [0,.0009*math.sin(math.pi*i/24)]:
            zz=z+dz;y=-.060-math.sqrt(max(.000001,.022**2-dx*dx-(zz-.177)**2))-.0015
            v.append((x,y,zz))
    eyes.append(mesh('RCL_Borda_Palpebra_'+key,v,[facing((2*i,2*i+1,2*i+3,2*i+2),v) for i in range(24)],brown,True,key+'-margin'))

def nose_y(x,z):
    r2=(x/.0145)**2+((z-.146)/.025)**2
    fade=max(0,1-r2)**.5
    tip=.021*math.exp(-(x/.010)**2-((z-.137)/.009)**2)
    bridge=.014*math.exp(-(x/.0048)**2-((z-.152)/.017)**2)
    wings=sum(.010*math.exp(-((x-a)/.0048)**2-((z-.136)/.0055)**2) for a in [-.010,.010])
    return at(tree,x,z)-fade*(tip+bridge+wings)
nose=[patch('nose')]
print('NOSE_DONE',flush=True)
for sign in [-1,1]:nose.append(disc('RCL_Narina_'+str(sign),sign*.0086,.1328,.0022,.00105,lambda x,z:nose_y(x,z)-.00025,nostril,'nose-nostril-'+str(sign),16))

fixed_by_base={};chin=[0,-.001,.006,-.019,-.004]
for bi,b in enumerate(bases):
    print('FIXED',bi,flush=True)
    baseid=b['module_id'];t=surface(b);parts=[]
    # Brows and mouth follow the receiving skin; their visual design stays fixed.
    for sign in [-1,1]:
        shape=[(.016,.201),(.018,.210),(.048,.218),(.059,.215),(.043,.211),(.022,.204)]
        shape=[(sign*x,z) for x,z in shape];v=[(x,at(t,x,z)-d,z) for d in [.0006,.0023] for x,z in shape];n=len(shape)
        f=[tuple(range(n-1,-1,-1)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
        parts.append(mesh('RCL_Sobrancelha_'+baseid+'_'+str(sign),v,f,brown,False,baseid+'-brow-'+str(sign),baseid))
    mouthz=.116+chin[bi]*.30
    def mouthline(x):return mouthz+.0025*(1-(abs(x)/.020)**1.6)-.004*(abs(x)/.020)**2
    v=[];N=24
    for i in range(N+1):
        x=-.020+.040*i/N;fade=math.sin(math.pi*i/N)
        for offset,depth in [(.0020*fade,.0004),(0,.0018),(-.0032*fade,.0012)]:
            z=mouthline(x)+offset;v.append((x,at(t,x,z)-depth*fade-.0002,z))
    f=[]
    for i in range(N):
        for j in range(2):f.append(facing((i*3+j,(i+1)*3+j,(i+1)*3+j+1,i*3+j+1),v))
    parts.append(mesh('RCL_Labios_'+baseid,v,f,lip,True,baseid+'-lips',baseid))
    v=[]
    for i in range(N+1):
        x=-.020+.040*i/N;fade=math.sin(math.pi*i/N)
        for dz in [-.00045*fade,.00045*fade]:
            z=mouthline(x)+dz;v.append((x,at(t,x,z)-.0020*fade-.0003,z))
    parts.append(mesh('RCL_Boca_'+baseid,v,[facing((2*i,2*i+2,2*i+3,2*i+1),v) for i in range(N)],crease,True,baseid+'-mouth',baseid))
    for sign in [-1,1]:
        # Pinna bowl, front ring, recessed concha and back. Root embedded in the base.
        v=[];N=20
        for radius,y in [(1,-.027),(.76,-.035),(.44,-.025),(.15,-.023)]:
            for i in range(N):
                th=2*math.pi*i/N
                v.append((sign*(.081+.015*radius*math.cos(th)) ,y+.007*math.cos(th),.172+.027*radius*math.sin(th)))
        f=[]
        for k in range(3):
            for i in range(N):f.append((k*N+i,k*N+(i+1)%N,(k+1)*N+(i+1)%N,(k+1)*N+i))
        f.append(tuple(range(3*N,4*N)))
        back=len(v);v.append((sign*.081,-.003,.172))
        for i in range(N):f.append((i,back,(i+1)%N))
        ear=mesh('RCL_Orelha_'+baseid+'_'+str(sign),v,f,skin,True,baseid+'-ear-'+str(sign),baseid)
        ear.data.materials.append(earshade)
        for p in ear.data.polygons:
            if 2*N<=p.index<=3*N:p.material_index=1
        parts.append(ear)
    fixed_by_base[baseid]=parts
    # Shared original normal at each open edge on the base side.
    custom=[v.normal.copy() for v in b.data.vertices]
    for i in fixed:custom[i]=normals[i]
    b.data.normals_split_custom_set_from_vertices(custom)

def show(idx,hair_visible=True):
    hair.hide_render=not hair_visible;hair.hide_set(not hair_visible)
    for j,b in enumerate(bases):
        for o in [b,*fixed_by_base[b['module_id']]]:o.hide_render=j!=idx;o.hide_set(j!=idx)
show(0)
root['contract']='rcl-female-face-v2';root['source_completed']='conjunto-feminino-v1'
print('SAVING_BEFORE_PREVIEW',flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'conjunto-feminino-v2.blend'))
print('SAVED_BEFORE_PREVIEW',flush=True)
s.render.resolution_x=480;s.render.resolution_y=540;s.render.resolution_percentage=100;s.eevee.taa_render_samples=32
target=Vector((0,0,.165))
for name,pos,h in [('frente',(0,-.9,.165),True),('sem-cabelo',(0,-.9,.165),False),('perfil',(.9,0,.165),False),('tres-quartos',(.53,-.8,.29),True)]:
    show(0,h);s.camera.location=pos;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler()
    s.render.filepath=str(OUT/'previas'/('piloto-'+name+'.png'));bpy.ops.render.render(write_still=True)
show(0)
(OUT/'interfaces.json').write_text(json.dumps({k:{'source_indices':h['loop'],'positions':[list(source[i]) for i in h['loop']]} for k,h in holes.items()},indent=2),encoding='utf8')
(OUT/'escolhas.json').write_text(json.dumps({'source':'conjunto-feminino-v1','shared':['hair-f-01','eye-1 pair','nose-1'],'fixed_per_base':['eyebrows','mouth','ears'],'eye_center':[.037,-.060,.177],'eye_radius':.022,'mouth_z':.116,'mouth_chin_follow':.30,'standardized_interface_vertices':len(fixed),'scalp_preserved':True,'refs':[33,19,49,88]},indent=2),encoding='utf8')
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'conjunto-feminino-v2.blend'))
print('FACIAL_PREVIEW_SAVED',len(eyes),len(nose),flush=True)
