from hashlib import new
import os, random, shutil, json

# Blacklist for the textures. Add texture to the blacklist in blacklist.txt.
blacklist_file = open("blacklist.txt", "r")
blacklist_textures_list = []

for line in blacklist_file:
    stripped_line = line.strip()
    blacklist_textures_list.append(stripped_line)

blacklist_file.close()

# Generates a random resource pack name
new_pack_name = "resource_pack_" + str(random.randint(1,1000000))

# Creates the new resource pack directory
new_directory = "new_resources\\" + new_pack_name
os.makedirs(new_directory)

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


# Creates the correct pack.mcmeta and writes a fancy and distinghuised description
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

# Main event
def main():
    global blacklist_textures_list, new_pack_name, pack_version, new_directory

    # Selector for the subfolder of the textures to be randomized.
    subfolder_string_list = ""
    subfolders_list = [f.path for f in os.scandir("textures\\") if f.is_dir()]
    for i in range(len(subfolders_list)):
        subfolder_string_list = subfolder_string_list + subfolders_list[i] + "[" + str(i) + "] "

    while True:
        try:
            select_sub = int(input("Select the number of the texture subfolder you want to use (1-"+ str(len(subfolders_list)-1) + "): " + subfolder_string_list +"\n"))
            subfolder = subfolders_list[select_sub]
            if subfolder.startswith("textures\\block") == True:
                if pack_version < 2:
                    basepath = "blocks"
                else:
                    basepath = "block"
                break
            if subfolder.startswith("textures\\item") == True:
                if pack_version < 2:
                    basepath = "items"
                else:
                    basepath = "item"
                break
            else:
                print("Invalid subfolder name. The subfolder name has to start with either 'blocks' (for blocks textures) or 'items' (for items textures)")
        except ValueError:
            print("Please use a number to select the subfolder.")
        except IndexError:
            print("The subfolder doesn't exist or you have mistyped the number.")

    # Creates the new texture folder within the new resource pack
    new_texture_folder = new_directory + "\\assets\\minecraft\\textures\\" + basepath
    os.makedirs(new_texture_folder)

    # Creates a list of all the textures in the specified textures folder, without the blacklisted ones.
    textures_list = []
    with os.scandir(subfolder) as entries:
        for entry in entries:
            if entry.is_file():
                if entry.name in blacklist_textures_list:
                    blacklist_textures = shutil.copy(subfolder + "\\" + entry.name, new_texture_folder + "\\" + entry.name)
                    continue
                if entry.name.endswith(".png") != True:
                    blacklist_ends = shutil.copy(subfolder + "\\" + entry.name, new_texture_folder + "\\" + entry.name)
                    continue
                else:
                    textures_list.append(entry.name)

    # Shuffle the textures in a new list
    new_textures_list = textures_list.copy()
    random.shuffle(new_textures_list)

    # Creates the new textures folder within the new resource pack by associting the blocks textures to their new textures name
    for old,new in zip(textures_list,new_textures_list):
        new_textures = shutil.copy(subfolder+"\\"+old, new_texture_folder+"\\"+new)

    # Ending (or start-over)
    print("Done! You can find your new resource pack at: " + "new_ressources" + new_pack_name + "\n" + "Or you can add a new folder to your resource pack!")
    if str(input("Do you want to add a new texture folder ? Y for Yes, anything else to end. \n")) == "Y":
        main()
    else:
        os.system('pause')

if __name__ == "__main__":
    main()
