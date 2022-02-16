from PIL import Image
from itertools import product
import os

def tile(img, dir_out, d, IsWool):
    ext = ".png"
    w, h = img.size
    
    grid = list(product(range(0, h-h%d, d), range(0, w-w%d, d)))
    index = 0
    for i, j in grid:
        
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{index}{ext}')
        img.crop(box).save(out)
        index += 1
    properties = dir_out + "/" + file[:-4] + ".properties"
    path = os.path.join(properties)
    f = open(path, "w+")
    f.write("matchBlocks=" + block_id + "\n")
    f.write("method=ctm\n")
    f.write("tiles=0-46\n")
    if IsWool:
        carpet_properties = dir_out + "/" + file[:-4] + "_carpet.properties"
        carpet_path = os.path.join(carpet_properties)
        g = open(carpet_path, "w+")
        g.write()
        g.write("matchBlocks=" + block_id + "\n")
        g.write("method=ctm\n")
        g.write("tiles=0-46\n")

for file in os.listdir('blocks/'):

    IsWool = False
    if "wool_colored" in file:
        block_id = "minecraft:wool:color=" + file[13:-4]
        carpet_block_id = "minecraft:carpet:color=" + file[13:-4]
    else:
        block_id = "minecraft:" + file[:-4]
    
    if "wool" in file:
        IsWool = True

    if file in os.listdir('overlays/'):

# block_name = input("Nom du CTM ?")
# block_id = input("Block ID ?")
# dir_out = "result/" + block_name

        if not file[:-4] in os.listdir('result/'):
            os.mkdir("result/" + file[:-4])

        block = Image.open(f"blocks/{file}").copy().convert('RGBA')
        overlay = Image.open(f"overlays/{file}").copy().convert('RGBA')
        template = Image.open("assets/template.png").copy().convert('L')

        image1 = Image.new(mode="RGBA", size=(192, 64), color=0)
        edit = Image.new(mode="RGBA", size=(192, 64), color=0)


        for y in range(0, 4):
            for x in range(0, 12):
                image1.paste(block, ( x * 16, y * 16))

        backup = image1.copy()

        for y in range(0, 4):
            for x in range(0, 12):
                edit.paste(overlay, ( x * 16, y * 16), overlay)

        image1.paste(edit, (0, 0), edit)
        image1.paste(backup, (0, 0), template)

        dir_out = 'result/' + file[:-4]

        tile(image1, dir_out, 16, IsWool)