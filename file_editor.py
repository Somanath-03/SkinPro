import pandas as pd
import os

pd_reader = pd.read_csv("classes.csv") #reads csv but can read excel also and other file format
data = pd.DataFrame(pd_reader) # returns data in the form of table 

Acne,Normal_Skin,Blackheads,Dry_Skin,Dark_Skin,Dark_Spots,Eye_bags,Oily_Skin,Pores,Skin_Redness,Wrinkles=[],[],[],[],[],[],[],[],[],[],[]

# Define the directory path
directory = "./train"

# Get a list of filenames
filenames = os.listdir(directory)


for row in data.itertuples():
    print(row)
    if row._7:
        Normal_Skin.append(row.filename)
    if row._2:
        Acne.append(row.filename)
    if row._3:
        Blackheads.append(row.filename)
    if row._4:
        Dark_Spots.append(row.filename)
    if row._5:
        Dry_Skin.append(row.filename)
    if row._6:
        Eye_bags.append(row.filename)
    if row._8:
        Oily_Skin.append(row.filename)
    if row._9:
        Pores.append(row.filename)
    if row._10:
        Skin_Redness.append(row.filename)
    if row._11:
        Wrinkles.append(row.filename)
    
    
print(len(Dark_Skin))

k = 0
for i in filenames:
    k+=1
    try:
        if i in Acne:
            os.rename(f"./train/{i}",f"./acne/acne{k}.jpg")
        if i in Blackheads:
            os.rename(f"./train/{i}",f"./blackheads/blackheads{k}.jpg")
        if i in Dry_Skin:
            os.rename(f"./train/{i}",f"./dry_skin/dry_skin{k}.jpg")
        if i in Dark_Spots:
            os.rename(f"./train/{i}",f"./dark_spots/dark_spots{k}.jpg")
        if i in Eye_bags:
            os.rename(f"./train/{i}",f"./eye_bags/eye_bags{k}.jpg")
        if i in Normal_Skin:
            os.rename(f"./train/{i}",f"./normal_skin/normal_skin{k}.jpg")
        if i in Dark_Skin:
            os.rename(f"./train/{i}",f"./dark_skin/dark_skin{k}.jpg")
        if i in Oily_Skin:
            os.rename(f"./train/{i}",f"./oily_skin/oily_skin{k}.jpg")
        if i in Pores:
            os.rename(f"./train/{i}",f"./pores/pores{k}.jpg")
        if i in Skin_Redness:
            os.rename(f"./train/{i}",f"./skin_redness/skin_redness{k}.jpg")
        if i in Wrinkles:
            os.rename(f"./train/{i}",f"./wrinkles/wrinkles{k}.jpg")
    except:
        pass