import re
import copy
import csv
import xml.etree.ElementTree as ElementTree

# Default parameters for SVG multiplying

default_design_file = 'example_design.svg'  # Name of the original design file
default_data_file = 'example_data.csv'      # Name of the CSV data file

default_width = 900         # Width of the output SVG file in mm
default_height = 600        # Height of the output SVG file in mm
default_edge_margin = 15    # Margin at the outer edges of the output SVG file
default_inner_margin = 5    # Margin between design instances within the output SVG file


def prompt_value(prompt, prompt_type, default_value):
    """Helper function for prompting user for values of various types."""

    while True:
        output_value = input(prompt)    # Prompt user

        if output_value == '':
            # Select default value
            output_value = default_value
            break
        else:
            # Try typecasting, re-prompt user until successful
            try:
                output_value = prompt_type(output_value)
                break
            except ValueError:
                print("Invalid input type!")
                print()

    print()

    return output_value


def multiply_svg(design_file, data_file, output_width, output_height, edge_margin, inner_margin):
    """Multiplies the given SVG design using the input parameters."""

    pointer = [0, 0]
    file_counter = 1

    # Read CSV data to paste onto design copies
    csv_data = []
    with open(data_file, encoding='UTF-8') as csvfile:
        csvfile = csv.reader(csvfile, delimiter=',')
        for line in csvfile:
            csv_data.append(line)

    # Get the XML tree of the original design
    design_tree = ElementTree.parse(design_file)
    design_root = design_tree.getroot()

    # Read main namespace
    xml_namespace = '{' + design_root.tag.split('{')[1].split('}')[0] + '}'

    # Read dimensions of the original design
    width = float(design_root.get('width')[:-2])
    height = float(design_root.get('height')[:-2])

    # Set new dimensions
    design_root.set('width', f"{output_width}mm")
    design_root.set('height', f"{output_height}mm")
    design_root.set('viewBox', f"0 0 {output_width} {output_height}")

    # Save layers in original design
    design_layers = []
    for layer in design_root.findall(xml_namespace + 'g'):
        if layer.get('transform') is None:
            layer.set('transform', "translate(0,0)")

        design_layers.append(layer)
        design_root.remove(layer)

    # Make a new copy of the SVG design for each entry in the CSV data
    for line in csv_data:
        for layer in design_layers:
            # Make a recursive copy of the original layer
            new_layer = copy.deepcopy(layer)
            design_root.append(new_layer)

            # Move the new layer based on input parameters
            coords = [float(coord) for coord in new_layer.get('transform').split('(')[1].split(')')[0].split(',')]
            coords = (coords[0] + edge_margin + pointer[0] * width + pointer[0] * inner_margin,
                      coords[1] + edge_margin + pointer[1] * height + pointer[1] * inner_margin)
            new_layer.set('transform', f'translate({coords[0]},{coords[1]})')

            # Look for text elements to edit
            for text_element in new_layer.findall(xml_namespace + 'text'):
                if text_element.tag == xml_namespace + 'text':
                    label = text_element.get('{http://www.inkscape.org/namespaces/inkscape}' + 'label')
                    if label is not None and len(label.split('_')) > 1 and label.split('_')[0] == 'txt':
                        # Paste the correct text from CSV data
                        text_element.find(xml_namespace + 'tspan').text = line[int(label.split('_')[1]) - 1]

        # Move along rows and columns of the output SVG file until all the space is used up
        pointer[0] += 1
        if edge_margin + (pointer[0] + 1) * width + pointer[0] * inner_margin + edge_margin > output_width:
            pointer[0] = 0
            pointer[1] += 1
            if edge_margin + (pointer[1] + 1) * height + pointer[1] * inner_margin + edge_margin > output_height:
                # No more space in current output file --> Write out
                write_svg(design_root, file_counter)

                # Clear previous design copies
                for layer in design_root.findall(xml_namespace + 'g'):
                    design_root.remove(layer)

                # Reset pointer and move to next file
                pointer = [0, 0]
                file_counter += 1

    write_svg(design_root, file_counter)    # Write the final SVG output file


def write_svg(xml_root, file_counter):
    """Writes the given XML root content to an SVG file."""

    # Turn XML tree into a string
    xml_string = ElementTree.tostring(xml_root, encoding="UTF-8", xml_declaration=True).decode(encoding='UTF-8')

    # Remove main namespace mentions to fix the output SVG file
    xml_string = re.sub('ns0:', '', xml_string)
    xml_string = re.sub(':ns0', '', xml_string)

    # Write the finished XML string into an SVG file
    with open(f"output_{file_counter}.svg", "w", encoding='UTF-8') as text_file:
        text_file.write(xml_string)

    print(f"Wrote file 'output_{file_counter}.svg'")


def main():
    """Function with main interface logic."""

    design_file = prompt_value("Please enter the name of the SVG design file (with file extension), "
                               f"or press ENTER for default ({default_design_file}): ",
                               str, default_design_file)

    data_file = prompt_value("Please enter the name of the CSV data file (with file extension), "
                             f"or press ENTER for default ({default_data_file}): ",
                             str, default_data_file)

    output_width = prompt_value("Please enter the width of the output SVG image (in mm), "
                                f"or press ENTER for default ({default_width} mm): ",
                                float, default_width)

    output_height = prompt_value("Please enter the height of the output SVG image (in mm), "
                                 f"or press ENTER for default ({default_height} mm): ",
                                 float, default_height)

    edge_margin = prompt_value("Please enter the edge margin of the output SVG image (in mm), "
                               f"or press ENTER for default ({default_edge_margin} mm): ",
                               float, default_edge_margin)

    inner_margin = prompt_value("Please enter the inner margin of the output SVG image (in mm), "
                                f"or press ENTER for default ({default_inner_margin} mm): ",
                                float, default_inner_margin)

    # Initiate SVG multiplication based on the input parameters
    multiply_svg(design_file, data_file, output_width, output_height, edge_margin, inner_margin)

    print("Done")


if __name__ == '__main__':
    main()
