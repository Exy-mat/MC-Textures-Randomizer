import os, random, shutil, json

def main():
    # Blacklist for the file types.
    Blacklisted_file_type = ".mcmeta"

    # Blacklist for the textures. Format : "texture_name.png". Commas in between textures.
    Blacklisted_blocks_textures = ["campfire_fire.png","fire_0.png","fire_1.png","kelp.png","kelp_plant.png"]
    Blacklisted_items_textures = []
    
    # Selector for the subfolder of the textures to be randomized.
    str_sub = ""
    subfolders = [f.path for f in os.scandir("textures\\") if f.is_dir()]
    for i in range(len(subfolders)):
        str_sub = str_sub + str(subfolders[i]) + "[" + str(i) + "] "
    
    while True:
        try:
            select_sub = int(input("Select the number of the texture subfolder you want to use (max "+ str(len(subfolders)-1) + "): " + str_sub+"\n"))
            basepath = subfolders[select_sub]
            break
        except ValueError: # If user doesn't use a number
            print("Please use a number to select the wanted subfolder.")
        except IndexError: # If user uses a bigger number than possible or a negative number
            print("The subfolder doesn't exist or you have mistyped the number.")
    
    # Creates a list of all the textures in the specified textures folder, without the blacklisted ones.
    block_textures_list = []
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

    # Creates the new ressource pack directory
    dirName = "new_ressources\\" + new_pack_name + "\\assets\\minecraft\\textures\\block"
    os.makedirs(dirName)

    # Creates the new ressources pack by associting the blocks to their new textures
    for old,new in zip(block_textures_list,new_block_textures_list):
        new_textures = shutil.copy(basepath+"\\"+old, dirName+"\\"+new)
    
    # Selector for the version of the ressource pack, for the pack.mcmeta
    while True:
        try:
            pack_version = int(input(
                "Please select the version of the ressource pack (1-7):\n"
                "Minecraft 1.6.1 - 1.8.9: [1]\n"
                "Minecraft 1.9 - 1.10.2: [2]\n"
                "Minecraft 1.11 - 1.12.2 : [3]\n"
                "Minecraft 1.13 - 1.14.4 : [4]\n"
                "Minecraft 1.15 - 1.16.1 : [5]\n"
                "Minecraft 1.16.2 - 1.16.5 : [6]\n"
                "Minecraft 1.17 : [7]\n"
            ))
            break
        except ValueError:
            print("Please use a number to select the ressource pack version.")
    
    pack_path = "new_ressources\\"+ new_pack_name
    pack_name = "pack.mcmeta"
    completePath = os.path.join(pack_path,pack_name)
    pack_format = {
        "pack": {
        "pack_format": pack_version,
        "description": "Randomly generated ressource pack"
        }
    }

    with open(completePath, "w") as pack_create:
        json.dump(pack_format, pack_create, indent=2)

if __name__ == "__main__":
    main()
