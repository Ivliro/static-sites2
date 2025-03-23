from textnode import TextNode, TextType
from gencontent import generate_page

import os
import shutil

def main():

    copy_directory_recursive('./static/','./public/')
    print("Generating page...")
    generate_page(
        os.path.join('./content', "index.md"),
        './template.html',
        os.path.join('./public', "index.html"),
    )

def copy_directory_recursive(source_dir, dest_dir):
    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    
    # Delete destination directory if it exists
    if os.path.exists(dest_dir):
        print(f"Cleaning destination directory: {dest_dir}")
        shutil.rmtree(dest_dir)
    
    # Create destination directory
    print(f"Creating destination directory: {dest_dir}")
    os.mkdir(dest_dir)
    
    # Get all items in source directory
    items = os.listdir(source_dir)
    
    # Copy each item in the source directory
    for item in items:
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        # If item is a file, copy it
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        # If item is a directory, recursively copy it
        else:
            print(f"Processing directory: {source_path}")
            copy_directory_recursive(source_path, dest_path)
    
    print(f"Finished copying directory: {source_dir} -> {dest_dir}")



main()