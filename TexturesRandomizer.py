import os, random, shutil, json

def main():
    # Blacklist for the file types.
    Blacklisted_file_type = [".mcmeta",".jpeg",".jpg",'.gif']

    # Blacklist for the textures. Add texture to the blacklist in blacklist.txt.
    blacklist_file = open("blacklist.txt", "r")
    blacklist_list = []
    
    for line in blacklist_file:
        stripped_line = line.strip()
        blacklist_list.append(stripped_line)

    blacklist_file.close()

    # Selector for the subfolder of the textures to be randomized.
    str_sub = ""
    subfolders = [f.path for f in os.scandir("textures\\") if f.is_dir()]
    for i in range(len(subfolders)):
        str_sub = str_sub + subfolders[i] + "[" + str(i) + "] "
    
    while True:
        try:
            select_sub = int(input("Select the number of the texture subfolder you want to use (max "+ str(len(subfolders)-1) + "): " + str_sub +"\n"))
            basepath = subfolders[select_sub]
            break
        except ValueError:
            print("Please use a number to select the wanted subfolder.")
        except IndexError:
            print("The subfolder doesn't exist or you have mistyped the number.")
    
    # Generates a new random name for the ressource pack
    new_pack_name = "resource_pack_" + str(random.randint(1,1000000))
    
    # Creates the new resource pack directory
    new_directory = "new_resources\\" + new_pack_name + "\\assets\\minecraft\\textures\\block"
    os.makedirs(new_directory)    
    
    # Creates a list of all the textures in the specified textures folder, without the blacklisted ones.
    textures_list = []
    with os.scandir(basepath) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name in blacklist_list:
                    blacklist_skip = shutil.copy(basepath + "\\" + entry.name, new_directory + "\\" + entry.name)
                    continue
                if entry.name.endswith(".mcmeta"):
                    blacklist_ends = shutil.copy(basepath + "\\" + entry.name, new_directory + "\\" + entry.name)
                    continue
                else:
                    textures_list.append(entry.name)
    
    # Shuffle the textures in a new list
    new_textures_list = textures_list.copy()
    random.shuffle(new_textures_list)

    # Creates the new resource pack by associting the blocks to their new textures
    for old,new in zip(textures_list,new_textures_list):
        new_textures = shutil.copy(basepath+"\\"+old, new_directory+"\\"+new)
    
    # Selector for the version of the resource pack, for the pack.mcmeta
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
            print("Please use a number to select the resource pack version.")
    
    # Adds the selected pack.mcmeta and the cool kid description
    description_text = "This is a randomly generated resource pack"
    random_description_text = ""
    hex_char = [1,2,3,4,5,6,7,8,9,"a","b","c","d","e","f"]
    for i in range(len(description_text)):
        random_description_text += "\u00A7"+ str(random.choice(hex_char)) + description_text[i] + "\u00A7r"
                                                       
    pack_path = "new_resources\\"+ new_pack_name
    pack_name = "pack.mcmeta"
    completePath = os.path.join(pack_path,pack_name)
    pack_format = {
        "pack": {
        "pack_format": pack_version,
        "description": random_description_text,
        }
    }

    with open(completePath, "w") as pack_create:
        json.dump(pack_format, pack_create, indent=2)
    
    # Ending
    print("Done, you can find your new resource pack : " + new_pack_name)
    os.system('pause')

if __name__ == "__main__":
    main()
