import os, random, shutil, json

# Code created by @Exymat#0001 on Discord, source code available at https://github.com/Exymat/Minecraft_Resource_pack_randomiser

# Blacklist for the textures. Add texture to the blacklist in blacklist.txt.
if os.path.isfile("blacklist.txt") == True:
    blacklist_file = open("blacklist.txt", "r")
    blacklist_textures_list = []

    for line in blacklist_file:
        stripped_line = line.strip()
        blacklist_textures_list.append(stripped_line)

    blacklist_file.close()

# Generates a random resource pack name
new_pack_name = "resource_pack_" + str(random.randint(1,1000000))

# Creates the new resource pack directory
new_resource_pack_folder = "resource_packs\\" + new_pack_name
os.makedirs(new_resource_pack_folder)

# Selector for the version of the resource pack, for the pack.mcmeta
while True:
    try:
        pack_version = int(input(
            "Please select the version of the ressource pack (1-7):\n"
            " Minecraft 1.6.1 - 1.8.9: [1]\n"
            " Minecraft 1.9 - 1.10.2: [2]\n"
            " Minecraft 1.11 - 1.12.2 : [3]\n"
            " Minecraft 1.13 - 1.14.4 : [4]\n"
            " Minecraft 1.15 - 1.16.1 : [5]\n"
            " Minecraft 1.16.2 - 1.16.5 : [6]\n"
            " Minecraft 1.17 : [7]\n"
            ))
        if pack_version <= 7:
            break
        else:
            print("Please use a number between 1 and 7 to select the resource pack version.")
    except ValueError:
        print("Please use a number to select the resource pack version.")


# Creates the correct pack.mcmeta and writes a fancy and distinghuised description
description_text = "This is a randomly generated resource pack"
random_description_text = ""
hex_char = [1,2,3,4,5,6,7,8,9,"a","b","c","d","e","f"]
for i in range(len(description_text)):
    random_description_text += "\u00A7"+ str(random.choice(hex_char)) + description_text[i] + "\u00A7r"

pack_name = "pack.mcmeta"
completePath = os.path.join(new_resource_pack_folder,pack_name)
pack_format = {
    "pack": {
    "pack_format": pack_version,
    "description": random_description_text,
    }
}

with open(completePath, "w") as pack_create:
    json.dump(pack_format, pack_create, indent=2)

# Main event
def main():
    global blacklist_textures_list, new_pack_name, pack_version, new_resource_pack_folder

    # Selector for the subfolder of the textures to be randomized.
    subfolders_list = [f.path for f in os.scandir("textures\\") if f.is_dir()]

    while True:
        try:
            print("Please select the subfolder to use :")
            print_list = [print(" "+subfolders_list[i] + ': [' + str(i) + ']') for i in range(len(subfolders_list))]
            subfolder = subfolders_list[int(input(""))]
            break
        except ValueError:
            print("Please use a number to select the subfolder.")
        except IndexError:
            print("The subfolder does not exist or you have mistyped the number.")
    while True:
        try:
            texture_type = int(input("Please select the textures type:\n Blocks : [0]\n Items : [1]\n"))
            if texture_type == 0:
                if pack_version < 1:
                    basepath = "blocks"
                else:
                    basepath = "block"
                break
            if texture_type == 1:
                if pack_version < 1:
                    basepath = "items"
                else:
                    basepath = "item"
                break
            else:
                print("Texture type does not exist or you have mistyped the number.")
        except ValueError:
            print("Please use a number to select the texture type.")

    # Creates the new texture folder within the new resource pack
    new_resource_pack_folder = new_resource_pack_folder + "\\assets\\minecraft\\textures\\" + basepath
    os.makedirs(new_resource_pack_folder)

    # Creates a list of all the textures in the specified textures folder, ignoring the blacklisted ones.
    textures_list = []
    with os.scandir(subfolder) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name in blacklist_textures_list:
                    blacklist_textures = shutil.copy(subfolder + "\\" + entry.name, new_resource_pack_folder + "\\" + entry.name)
                    continue
                if entry.name.endswith(".png") != True:
                    blacklist_ends = shutil.copy(subfolder + "\\" + entry.name, new_resource_pack_folder + "\\" + entry.name)
                    continue
                else:
                    textures_list.append(entry.name)

    # Shuffle the textures in a new list
    new_textures_list = textures_list.copy()
    random.shuffle(new_textures_list)

    # Associates the textures to their new textures name
    for old,new in zip(textures_list,new_textures_list):
        new_textures = shutil.copy(subfolder+"\\"+old, new_resource_pack_folder+"\\"+new)

    # User prompt to end or start again with another folder
    print("Done, your new resource pack is: " + new_pack_name + "\n")
    repeat = str(input("Do you want to add a new folder to your resource pack? Y/y for Yes, anything else to end. \n"))
    if repeat == "Y" or repeat == "y":
        main()
    else:
        os.system('pause')

if __name__ == "__main__":
    main()
