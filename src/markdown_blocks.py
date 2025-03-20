from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    # Split the markdown by double newlines
    blocks = markdown.split("\n\n")
    
    # Process each block
    result = []
    for block in blocks:
        # Strip leading/trailing whitespace
        stripped_block = block.strip()
        
        # Only add non-empty blocks
        if stripped_block:
            result.append(stripped_block)
    
    return result

def block_to_block_type(block):
    # Check if the block is empty
    if not block:
        return BlockType.PARAGRAPH
    
    # Split the block into lines for multi-line checks
    lines = block.split("\n")
    first_line = lines[0]
    
    # Check for heading (starts with 1-6 # characters followed by a space)
    if first_line.startswith(("#", "##", "###", "####", "#####", "######")):
        # Make sure the # is followed by a space
        heading_marker = first_line.split(" ")[0]
        if 1 <= len(heading_marker) <= 6 and all(c == '#' for c in heading_marker):
            return BlockType.HEADING
    
    # Check for code block (starts and ends with ```)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by a space)
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    # Check for ordered list (every line starts with a number followed by . and a space)
    if all(line.strip() and line[0].isdigit() and line.find(". ") > 0 for line in lines):
        # Check if numbers start at 1 and increment by 1
        numbers = [int(line.split(". ")[0]) for line in lines]
        if numbers[0] == 1 and all(numbers[i] == numbers[i-1] + 1 for i in range(1, len(numbers))):
            return BlockType.OLIST
    
    # Default to paragraph if none of the above conditions are met
    return BlockType.PARAGRAPH