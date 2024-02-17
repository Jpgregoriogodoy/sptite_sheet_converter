import os
from PIL import Image
from tkinter import filedialog
import tkinter as tk
from tqdm import tqdm

# File select logic
def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        return file_path
    else:
        print("No file selected. Exiting.")
        exit()

# Converts the sprite sheet from a 4 column to a 3 column sprite sheet
def convert_image_4to3(file_path):
    img = Image.open(file_path)
    width = img.width
    col_width = width // 4
    columns = []
    for col in tqdm(range(4),ncols=100):
        left_border = col * col_width
        top_border = 0
        right_border = left_border + col_width
        bottom_border = top_border + img.height
        sub_img = img.crop((left_border, top_border, right_border, bottom_border))
        columns.append(sub_img)
    columns = columns[1:4]
    full_image = Image.new('RGBA', (sum(col.width for col in columns), columns[0].height))
    x_offset = 0
    for col in columns:
        full_image.paste(col, (x_offset, 0))
        x_offset += col.width

    # Save the result
    input_dir = os.path.dirname(file_path)
    output = f"{input_dir}/output/MV_Spritesheet.png"
    if not os.path.exists(os.path.dirname(output)):
        os.mkdir(os.path.dirname(output))
    full_image.save(output)  # Save the result 


# Converts the sprite sheet from a 3 column to a 4 column sprite sheet
# Converts the sprite sheet from a 3 column to a 4 column sprite sheet
def convert_image_3to4(file_path):
    img = Image.open(file_path)
    width = img.width
    height = img.height
    col_width = width // 3
    sub_col_width = width // 12
    sub_col_height = height //2
    
    

    # Ask the user whether it's a single character sheet or 8 characters in a single sheet
    sheet_type = input("Is it a single character sheet (enter '1') or 8 characters in a single sheet (enter '8')? ")

    if sheet_type == '1':     
        columns = []
        for col in tqdm(range(3), ncols=100):
            left_border = col * col_width
            top_border = 0
            right_border = left_border + col_width
            bottom_border = top_border + img.height
            sub_img = img.crop((left_border, top_border, right_border, bottom_border))
            columns.append(sub_img)
        columns.insert(0, columns[1])
        full_image = Image.new('RGBA', (sum(col.width for col in columns), columns[0].height))
        x_offset = 0
        for col in columns:
            full_image.paste(col, (x_offset, 0))
            x_offset += col.width

        # Save the result
        input_dir = os.path.dirname(file_path)
        output = f"{input_dir}/output/XP_Spritesheet.png"
        if not os.path.exists(os.path.dirname(output)):
            os.mkdir(os.path.dirname(output))
        full_image.save(output)  # Save the result  

    elif sheet_type == '8':
        # Convert each character separately
        iteration = 0
        for row in range(2):
            for col in tqdm(range(4),ncols=100):
                iteration += 1
                left_border = col * (width//4)
                top_border = row * (height // 2)
                right_border = left_border + (width//4)
                bottom_border = top_border + (height // 2)
                sub_img = img.crop((left_border, top_border, right_border, bottom_border))
                columns = []
                for col in range(3):
                    left_border = col * sub_col_width
                    top_border = 0
                    right_border = left_border + sub_col_width
                    bottom_border = top_border + sub_col_height
                    char_sub_img = sub_img.crop((left_border, top_border, right_border, bottom_border))

                    columns.append(char_sub_img)
                columns.insert(0, columns[1])
                full_image = Image.new('RGBA', (sum(col.width for col in columns), columns[0].height))
                x_offset = 0
                for col in columns:
                    full_image.paste(col, (x_offset, 0))
                    x_offset += col.width

                # Save the result
                input_dir = os.path.dirname(file_path)
                output = f"{input_dir}/output/XP_Spritesheet_{iteration}.png"
                if not os.path.exists(os.path.dirname(output)):
                    os.mkdir(os.path.dirname(output))
                full_image.save(output)  # Save the result  
                
                
    else:
        print("Invalid selection. Exiting.")
        exit()
  


root = tk.Tk()
root.withdraw()

input_file_path = open_file_dialog()

user_selection = ""
valid_selection = ["1","2","3->4","4->3"]

while user_selection not in valid_selection:   
    print("Plese select the conversion method:\n\n1. 3->4\n\n2. 4->3")
    user_selection = input("Selection: ").lower()
    if user_selection not in valid_selection:
        print("\ninvalid selection\n")

if user_selection in ["2","4->3"]:
    convert_image_4to3(input_file_path)
else:
    convert_image_3to4(input_file_path)

#open output folder after conversion
output_folder = os.path.dirname(input_file_path)
os.startfile(output_folder)

