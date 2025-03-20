def markdown_to_blocks(markdown):
    """
    Split a markdown string into block strings based on blank lines.
    
    Args:
        markdown (str): A string containing markdown content
        
    Returns:
        list: A list of strings, each representing a markdown block
    """
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