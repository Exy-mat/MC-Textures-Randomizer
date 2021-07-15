import os, random, shutil

def main():
    # Blacklist
    Blacklisted_file_type = ".mcmeta"

    # Add a block texture to the blacklist. Format : "block_texture_name.png". Commas in between block textures.
    Blacklisted_blocks_textures = ["campfire_fire.png","fire_0.png","fire_1.png","kelp.png","kelp_plant.png"]

    # Creates a list of all the textures in the textures\block folder, without the blacklisted ones.
    block_textures_list = []

    basepath = "textures\\block"
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name in Blacklisted_blocks_textures:
                    pass
                if entry.name.endswith(Blacklisted_file_type) == True:
                    pass
                else:
                    block_textures_list.append(entry.name)
                    
    # Generates a new random name for the ressource pack
    new_pack_name = "ressources_pack_" + str(random.randint(1,1000000))

    # Shuffle the textures in a new list
    new_block_textures_list = block_textures_list.copy()
    random.shuffle(new_block_textures_list)

    # Creates the new ressources pack directory and paste the pck.mcmeta
    dirName = "new_ressources\\" + new_pack_name + "\\assets\\minecraft\\textures\\block"
    os.makedirs(dirName)
    Add_pack = shutil.copy("pack.mcmeta", "new_ressources\\" + new_pack_name + "\\")

    # Creates the new ressources pack by associting the blocks to their new textures
    for old,new in zip(block_textures_list,new_block_textures_list):
        new_block_texture = shutil.copy(basepath+"\\"+old, dirName+"\\"+new)

if __name__ == "__main__":
    main()