import bpy, bmesh, math, sys, os
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.join(HERE, 'tex')
OUT = os.path.join(HERE, 'renders')
os.makedirs(OUT, exist_ok=True)
args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SHOT = args[0] if args else 'hero_mg'
SAMPLES = int(args[1]) if len(args) > 1 else 128
SCALE = float(args[2]) if len(args) > 2 else 1.0

L, W, H = 0.125, 0.105, 0.075   # box, metres
SW, SH = 0.050, 0.070           # sachet

bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.engine = 'CYCLES'
scn.cycles.device = 'CPU'
scn.cycles.samples = SAMPLES
scn.cycles.use_denoising = True
scn.cycles.max_bounces = 8
scn.view_settings.view_transform = 'AgX'
scn.view_settings.look = 'AgX - Punchy'
scn.view_settings.exposure = -0.7
scn.render.film_transparent = False

def img(name):
    p = os.path.join(TEX, name)
    i = bpy.data.images.load(p, check_existing=True)
    return i

def principled(name, color=(1, 1, 1, 1), rough=0.5, tex=None, alpha_tex=None, bump=None, coat=0.0, sss=0.0, noncolor_alpha=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; n = nt.nodes; l = nt.links
    bsdf = n['Principled BSDF']; out = n['Material Output']
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = rough
    bsdf.inputs['Coat Weight'].default_value = coat
    bsdf.inputs['Coat Roughness'].default_value = 0.25
    if sss:
        bsdf.inputs['Subsurface Weight'].default_value = sss
        bsdf.inputs['Subsurface Radius'].default_value = (0.002, 0.002, 0.002)
        bsdf.inputs['Subsurface Scale'].default_value = 0.002
    shader = bsdf
    if tex:
        t = n.new('ShaderNodeTexImage'); t.image = img(tex); t.interpolation = 'Cubic'
        l.new(t.outputs['Color'], bsdf.inputs['Base Color'])
        if tex.endswith('_top.png'):
            tr = n.new('ShaderNodeBsdfTransparent'); mix = n.new('ShaderNodeMixShader')
            l.new(t.outputs['Alpha'], mix.inputs['Fac'])
            l.new(tr.outputs[0], mix.inputs[1]); l.new(bsdf.outputs[0], mix.inputs[2])
            shader = mix
    if alpha_tex:
        a = n.new('ShaderNodeTexImage'); a.image = img(alpha_tex); a.image.colorspace_settings.name = 'Non-Color'
        tr = n.new('ShaderNodeBsdfTransparent'); mix = n.new('ShaderNodeMixShader')
        l.new(a.outputs['Color'], mix.inputs['Fac'])
        l.new(tr.outputs[0], mix.inputs[1]); l.new(shader.outputs[0], mix.inputs[2])
        shader = mix
    if bump:
        bt = n.new('ShaderNodeTexImage'); bt.image = img(bump); bt.image.colorspace_settings.name = 'Non-Color'
        bn = n.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.15; bn.inputs['Distance'].default_value = 0.00003
        l.new(bt.outputs['Color'], bn.inputs['Height']); l.new(bn.outputs['Normal'], bsdf.inputs['Normal'])
    l.new(shader.outputs[0], out.inputs['Surface'])
    return m

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*c, a)

def link(o):
    bpy.context.collection.objects.link(o); return o

# ---------------- objects ----------------
def make_box(prod, loc=(0, 0, 0), rotz=0.0, with_sachets=True, used=3):
    me = bpy.data.meshes.new('box_' + prod); bm = bmesh.new(); uv = bm.loops.layers.uv.new()
    x0, x1, y0, y1 = -L / 2, L / 2, -W / 2, W / 2
    faces = {
        'front': [(x0, y0, 0), (x1, y0, 0), (x1, y0, H), (x0, y0, H)],
        'back': [(x1, y1, 0), (x0, y1, 0), (x0, y1, H), (x1, y1, H)],
        'sideA': [(x1, y0, 0), (x1, y1, 0), (x1, y1, H), (x1, y0, H)],
        'sideB': [(x0, y1, 0), (x0, y0, 0), (x0, y0, H), (x0, y1, H)],
        'top': [(x0, y0, H), (x1, y0, H), (x1, y1, H), (x0, y1, H)],
        'bottom': [(x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, 0)],
    }
    order = list(faces)
    ob = bpy.data.objects.new('box_' + prod, me)
    for i, k in enumerate(order):
        vs = [bm.verts.new(v) for v in faces[k]]
        f = bm.faces.new(vs); f.material_index = i
        for lp, (u, v) in zip(f.loops, [(0, 0), (1, 0), (1, 1), (0, 1)]):
            lp[uv].uv = (u, v)
        ob.data.materials.append(principled(f'{prod}_{k}', tex=f'{prod}_{k}.png', rough=0.62, coat=0.08))
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bm.to_mesh(me); bm.free()
    link(ob)
    bev = ob.modifiers.new('bev', 'BEVEL'); bev.width = 0.0007; bev.segments = 3; bev.limit_method = 'ANGLE'
    ob.location = loc; ob.rotation_euler[2] = rotz
    # inner liner (white board) without top
    li = bpy.data.meshes.new('liner'); bm = bmesh.new()
    e = 0.0012
    a0, a1, b0, b1 = x0 + e, x1 - e, y0 + e, y1 - e
    for quad in [[(a0, b0, e), (a0, b1, e), (a1, b1, e), (a1, b0, e)],
                 [(a0, b0, e), (a1, b0, e), (a1, b0, H - e), (a0, b0, H - e)],
                 [(a1, b1, e), (a0, b1, e), (a0, b1, H - e), (a1, b1, H - e)],
                 [(a1, b0, e), (a1, b1, e), (a1, b1, H - e), (a1, b0, H - e)],
                 [(a0, b1, e), (a0, b0, e), (a0, b0, H - e), (a0, b1, H - e)]]:
        bm.faces.new([bm.verts.new(v) for v in quad])
    bm.to_mesh(li); bm.free()
    lo = link(bpy.data.objects.new('liner', li)); lo.parent = ob
    lo.data.materials.append(principled('board', hexc('#EFE9DF'), 0.8))
    # PET film
    fm = bpy.data.meshes.new('film'); bm = bmesh.new()
    fx, fy = (L - 0.012) / 2, (W - 0.012) / 2
    bm.faces.new([bm.verts.new(v) for v in [(-fx, -fy, H - 0.0004), (fx, -fy, H - 0.0004), (fx, fy, H - 0.0004), (-fx, fy, H - 0.0004)]])
    bm.to_mesh(fm); bm.free()
    fo = link(bpy.data.objects.new('film', fm)); fo.parent = ob
    m = bpy.data.materials.new('pet'); m.use_nodes = True; n = m.node_tree.nodes; lk = m.node_tree.links
    n.remove(n['Principled BSDF'])
    tr = n.new('ShaderNodeBsdfTransparent'); gl = n.new('ShaderNodeBsdfGlossy'); gl.inputs['Roughness'].default_value = 0.04
    fr = n.new('ShaderNodeFresnel'); fr.inputs['IOR'].default_value = 1.4
    mix = n.new('ShaderNodeMixShader'); lk.new(fr.outputs[0], mix.inputs['Fac'])
    lk.new(tr.outputs[0], mix.inputs[1]); lk.new(gl.outputs[0], mix.inputs[2]); lk.new(mix.outputs[0], n['Material Output'].inputs['Surface'])
    fo.data.materials.append(m)
    if with_sachets:
        smat = principled('inner_sachet_' + prod, hexc('#F3EDE2'), 0.38, coat=0.25)
        band = principled('inner_band_' + prod, hexc({'mg': '#B0204F', 'ashwa': '#5A1A2C', 'moringa': '#2F5D50', 'shilajit': '#C8553D'}[prod]), 0.4, coat=0.2)
        n_per = 15; pitch = (L - 0.008) / n_per
        for r, yc in enumerate((-W / 4 + 0.0005, W / 4 - 0.0005)):
            for i in range(n_per):
                if r == 1 and i >= n_per - used:
                    continue
                bpy.ops.mesh.primitive_cube_add(size=1)
                s = bpy.context.active_object
                s.scale = (pitch * 0.82, SW * 0.97, SH * 0.98)
                s.location = (-L / 2 + 0.004 + pitch * (i + 0.5), yc, 0.0015 + SH * 0.49)
                s.rotation_euler = (0, math.radians((i % 3 - 1) * 1.5), 0)
                bpy.ops.object.transform_apply(scale=True)
                s.data.materials.append(smat); s.data.materials.append(band)
                # colour band on top crimp edge
                for poly in s.data.polygons:
                    if poly.normal.z > 0.9:
                        poly.material_index = 1
                b2 = s.modifiers.new('b', 'BEVEL'); b2.width = 0.0008; b2.segments = 2
                s.parent = ob
    return ob

def capsule_profile(x, y, caps, r=0.0060):
    best = 0.0
    for (cx, cy, half) in caps:
        dy = max(0.0, abs(y - cy) - half)
        d = math.hypot(x - cx, dy)
        if d < r:
            best = max(best, math.sqrt(1 - (d / r) ** 2))
    return best

def make_sachet(prod, name='sachet'):
    nx, ny = 100, 140
    me = bpy.data.meshes.new(name); bm = bmesh.new(); uv = bm.loops.layers.uv.new()
    ax0, ax1, ay0, ay1 = 0.005, SW - 0.005, 0.005, SH - 0.008
    caps = [(SW / 2 - 0.0062, 0.026, 0.0072), (SW / 2 + 0.0062, 0.026, 0.0072)]
    def bulge(x, y):
        if not (ax0 < x < ax1 and ay0 < y < ay1):
            return 0.0
        ex = math.sin(math.pi * (x - ax0) / (ax1 - ax0)); ey = math.sin(math.pi * (y - ay0) / (ay1 - ay0))
        env = (ex * ey) ** 0.45
        return env * (0.0010 + 0.0017 * capsule_profile(x, y, caps))
    grid = {}
    for side in (1, -1):
        for j in range(ny + 1):
            for i in range(nx + 1):
                x = SW * i / nx; y = SH * j / ny
                grid[(side, i, j)] = bm.verts.new((x - SW / 2, side * (bulge(x, y) + 0.00012), y))
    for side, mi in ((1, 0), (-1, 1)):
        for j in range(ny):
            for i in range(nx):
                q = [grid[(side, i, j)], grid[(side, i + 1, j)], grid[(side, i + 1, j + 1)], grid[(side, i, j + 1)]]
                if side == 1:
                    q = q[::-1]
                f = bm.faces.new(q); f.material_index = mi; f.smooth = True
                for lp in f.loops:
                    co = lp.vert.co; u = (co.x + SW / 2) / SW; v = co.z / SH
                    lp[uv].uv = (u if side == -1 else 1 - u, v) if False else ((1 - u) if side == 1 else u, v)
    bm.to_mesh(me); bm.free()
    ob = link(bpy.data.objects.new(name, me))
    ob.data.materials.append(principled(f'{prod}_sf', tex=f'{prod}_sfront.png', alpha_tex='sachet_alpha.png', bump='sachet_bump.png', rough=0.45, coat=0.12))
    ob.data.materials.append(principled(f'{prod}_sb', tex=f'{prod}_sback.png', alpha_tex='sachet_alpha.png', bump='sachet_bump.png', rough=0.45, coat=0.12))
    return ob

def fix_sachet_uv(ob):
    # front faces (material 0) face -y? ensure readable: we built front at +y bulge; view from -y needs mirrored u
    pass

_capmat = None
def make_capsule(loc, rot):
    global _capmat
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=32, radius=0.00425)
    c = bpy.context.active_object
    for v in c.data.vertices:
        v.co.z += 0.0074 if v.co.z > 0 else -0.0074
    bpy.ops.object.shade_smooth()
    if _capmat is None:
        _capmat = principled('capsule', hexc('#F4F1EA'), 0.3, coat=0.4, sss=0.25)
    c.data.materials.append(_capmat)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.00428, minor_radius=0.00018, location=(0, 0, 0.0035))
    t = bpy.context.active_object; t.data.materials.append(_capmat); t.parent = c
    c.location = loc; c.rotation_euler = rot
    return c

def make_cove(color='#DDD3C6'):
    me = bpy.data.meshes.new('cove'); bm = bmesh.new()
    prof = []
    for k in range(40):
        prof.append((-1.2 + k * (1.4 / 39), 0.0))
    R = 0.35
    for k in range(1, 25):
        a = math.pi / 2 * k / 24
        prof.append((0.2 + R * math.sin(a), R - R * math.cos(a)))
    for k in range(1, 20):
        prof.append((0.2 + R, R + k * 0.08))
    xs = [-2.5 + i * 0.25 for i in range(21)]
    rows = [[bm.verts.new((x, y, z)) for (y, z) in prof] for x in xs]
    for a in range(len(xs) - 1):
        for b in range(len(prof) - 1):
            f = bm.faces.new([rows[a][b], rows[a][b + 1], rows[a + 1][b + 1], rows[a + 1][b]]); f.smooth = True
    bm.normal_update(); bm.to_mesh(me); bm.free()
    o = link(bpy.data.objects.new('cove', me))
    m = principled('cove', hexc(color), 0.75)
    nt = m.node_tree; n = nt.nodes
    noise = n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value = 300
    bn = n.new('ShaderNodeBump'); bn.inputs['Strength'].default_value = 0.05
    nt.links.new(noise.outputs['Fac'], bn.inputs['Height']); nt.links.new(bn.outputs['Normal'], n['Principled BSDF'].inputs['Normal'])
    o.data.materials.append(m)
    # make sure normals face up / toward camera
    for p in o.data.polygons:
        pass
    return o

def area(name, loc, target, size, power, color=(1, 0.985, 0.96)):
    ld = bpy.data.lights.new(name, 'AREA'); ld.size = size; ld.energy = power; ld.color = color
    o = link(bpy.data.objects.new(name, ld)); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return o

def camera(loc, target, lens=85, fstop=5.6, focus=None):
    cd = bpy.data.cameras.new('cam'); cd.lens = lens
    o = link(bpy.data.objects.new('cam', cd)); o.location = loc
    d = Vector(target) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    cd.dof.use_dof = True; cd.dof.aperture_fstop = fstop
    cd.dof.focus_distance = focus or d.length
    scn.camera = o
    return o

def world(color='#EFE6DA', strength=0.08):
    w = bpy.data.worlds.new('w'); scn.world = w; w.use_nodes = True
    bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = hexc(color); bg.inputs['Strength'].default_value = strength

# ---------------- shots ----------------
def lights(k=1.0):
    area('key', (-0.55, -0.55, 0.65), (0, 0, 0.04), 0.45, 34 * k)
    area('fill', (0.75, -0.35, 0.30), (0, 0, 0.04), 1.0, 5 * k, (0.95, 0.97, 1.0))
    area('rim', (0.25, 0.55, 0.55), (0, 0, 0.05), 0.5, 22 * k)

world()
if SHOT.startswith('hero'):
    prod = SHOT.split('_')[1]
    make_cove()
    rz = math.radians(-10)
    box = make_box(prod, (0, 0, 0), rz)
    n = Vector((math.sin(rz) * 1, -math.cos(rz), 0)); n = Vector((-math.sin(-rz) if False else math.sin(rz), -math.cos(rz), 0))
    t = Vector((math.cos(rz), math.sin(rz), 0))
    fc = Vector((math.sin(rz) * W / 2, -math.cos(rz) * W / 2, 0))
    base = fc + t * 0.043 + n * 0.024
    s1 = make_sachet(prod, 's1'); s1.rotation_euler = (math.radians(18), 0, math.pi + rz); s1.location = (base.x, base.y, 0.0)
    s2 = make_sachet(prod, 's2'); s2.rotation_euler = (math.radians(90), 0, math.pi + math.radians(14)); s2.location = (-0.075, -0.125, 0.0043)
    make_capsule((0.005, -0.14, 0.00425), (math.radians(90), 0, math.radians(30)))
    make_capsule((0.03, -0.152, 0.00425), (math.radians(90), 0, math.radians(-55)))
    lights()
    camera((0.19, -0.39, 0.27), (-0.005, -0.05, 0.03), lens=60, fstop=8)
    scn.render.resolution_x, scn.render.resolution_y = int(1600 * SCALE), int(2000 * SCALE)
elif SHOT == 'lineup':
    make_cove()
    prods = ['mg', 'ashwa', 'moringa', 'shilajit']
    for i, p in enumerate(prods):
        make_box(p, (-0.24 + i * 0.16, 0.02 + (0.015 if i % 2 else 0), 0), math.radians(-12))
        s = make_sachet(p, 's_' + p)
        s.rotation_euler = (math.radians(90), 0, math.radians(180 + (i - 1.5) * 6))
        s.location = (-0.24 + i * 0.16 + 0.01, -0.105, 0.0046)
    lights(1.3)
    camera((0.0, -1.0, 0.40), (0.0, -0.03, 0.03), lens=62, fstop=11)
    scn.render.resolution_x, scn.render.resolution_y = int(2400 * SCALE), int(1500 * SCALE)
elif SHOT.startswith('sachets'):
    prod = SHOT.split('_')[1]
    make_cove()
    a = make_sachet(prod, 'a'); a.rotation_euler = (math.radians(90), 0, math.radians(174)); a.location = (-0.03, 0.0, 0.0037)
    b = make_sachet(prod, 'b'); b.rotation_euler = (math.radians(-90), 0, math.radians(-8)); b.location = (0.032, 0.008, 0.0037)
    make_capsule((-0.004, -0.052, 0.00425), (math.radians(90), 0, math.radians(20)))
    make_capsule((0.016, -0.056, 0.00425), (math.radians(90), 0, math.radians(-40)))
    lights(0.8)
    camera((0.0, -0.215, 0.36), (0.002, 0.004, 0.0), lens=100, fstop=8)
    scn.render.resolution_x, scn.render.resolution_y = int(1600 * SCALE), int(2000 * SCALE)

scn.render.filepath = os.path.join(OUT, f'{SHOT}.png')
scn.render.image_settings.file_format = 'PNG'
scn.cycles.threads = 4
scn.render.threads_mode = 'FIXED'; scn.render.threads = 4
bpy.ops.render.render(write_still=True)
print('RENDERED', scn.render.filepath)
