from glob import glob
from pathlib import Path

def bear_to_notion(source_folder: str = 'bear_notes',
                   dst_folder: str = 'changed_notes') -> None:
    """Convert Bear notes in markdown format to Notion formats. It mainly
    remove the tags

    Args:
        source_folder (str, optional): [description]. Defaults to 'bear_notes'.
        dst_folder (str, optional): [description]. Defaults to 'changed_notes'.
    """
    file_list = glob("bear_notes/*.md")
    
    for file in file_list:
        
        output = ""
        title = ""

        with open(file) as input_file:
            
            # write the first line directly because it's often the date
            output += next(input_file)
            title = output

            tabed_line = False
            
            block_tag = False
            tag = ""
            for line in input_file:
                tab_count = 0

                # check if this is in a list
                if line[0].isdigit():
                    tabed_line = True


                # take out leading # because it won't process indentations with
                # learning "#"
                if line.startswith('#') and not block_tag:
                    tag += line
                
                # process the code blocks by indentation
                elif line.startswith('```') and not block_tag and tabed_line:
                    output += f"{tab_string}{line}"
                    block_tag = True
                elif line.startswith('```') and block_tag and tabed_line:
                    output += f"{tab_string}{line}"
                    block_tag = False
                elif block_tag and tabed_line:
                    output += f"{tab_string}{line}"
                else:
                    output += line

                    # count how many tabs are there to indent code properly
                    tab_count = line.count("\t")
                    tab_string = "\t" * tab_count

            # print tag at the end
            if tag:
                output += f"\n\ntags: {tag}"
        
        # write to output file
        # take out first "# " char
        no_hash_title = title[2:].replace("\n","")

        # if first letter is a number
        if no_hash_title[0].isdigit() and "/" in no_hash_title:
            tokens = no_hash_title.split("/")
            # sometimes the year is 4 letters long
            if len(tokens[2]) == 4:
                changed_title = f"{tokens[2]}-{tokens[0]}-{tokens[1]}"
            else:
                changed_title = f"20{tokens[2]}-{tokens[0]}-{tokens[1]}"
            dst_file = Path(dst_folder) / Path(f"{changed_title}.md")
        else:
            dst_file = Path(dst_folder) / Path(f"{no_hash_title}.md")

        with open(dst_file, "w") as output_file:
            output_file.write(output)

                

                
def main():
    bear_to_notion()

if __name__ == "__main__":
    main()