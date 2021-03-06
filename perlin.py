import bpy
import math

# Global props - render path and number of frames to render
render_path = '/home/juniorxsound/Desktop/perlin/'
num_frames = 210

# Set global rendering props
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.resolution_x = 500
bpy.context.scene.render.resolution_y = 500
bpy.context.scene.render.resolution_percentage = 100

# Delete the default lamp and default cube
bpy.ops.object.select_all(action='DESELECT')
if bpy.data.objects.get('Lamp') is not None:
    bpy.data.objects['Lamp'].select = True
if bpy.data.objects.get('Cube') is not None:
    bpy.data.objects['Cube'].select = True
bpy.ops.object.delete()

# Set the cam in a top shot
cam = bpy.data.objects['Camera']
cam.location = (0,0,20)
cam.rotation_euler = (0,0,0)

# Create a grid
bpy.ops.mesh.primitive_grid_add(x_subdivisions=500, y_subdivisions=500, radius=10, view_align=False, enter_editmode=False, location=(0,0,0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

# Save the object
grid = bpy.data.objects['Grid']

# Create the displacement modfier
grid_mod = grid.modifiers.new(name='NoiseDisplacement', type='DISPLACE')
grid_mod.mid_level = 0

# Create new texture
bpy.ops.texture.new()
tex = bpy.data.textures.get('Texture')

# Set the displacement algorithem
tex.type = 'CLOUDS'

# Set the noise props
bpy.data.textures["Texture"].noise_basis = 'ORIGINAL_PERLIN'
bpy.data.textures["Texture"].noise_type = 'HARD_NOISE'
bpy.data.textures["Texture"].noise_depth = 0.3
bpy.data.textures["Texture"].noise_scale = 1.90

# Assign the texture to the displacement modifier
grid_mod.texture = tex

# Add a lighting
bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location=(0,0,5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))

# Keep track of current frame
current_frame = 0

bpy.ops.object.select_all(action='DESELECT')

# Render loop
while(current_frame < num_frames):

    #Render
    bpy.data.textures["Texture"].contrast = (math.sin(current_frame * 0.01) + 1) / 2
    bpy.data.textures["Texture"].intensity =  (math.sin(current_frame * 0.05) + 1) / 2

    file_name = 'frame_{}.png'.format(current_frame)
    bpy.data.scenes['Scene'].render.filepath = render_path + file_name
    bpy.ops.render.render( write_still=True )

    #Next frame please...
    current_frame += 1
