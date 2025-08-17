import graphviz
import os

def render_diagrams(diagram_codes, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    image_paths = []
    for i, code in enumerate(diagram_codes):
        dot = graphviz.Source(code)
        img_path = os.path.join(output_dir, f"diagram_{i+1}")
        dot.format = 'png'
        dot.render(filename=img_path, cleanup=True)
        image_paths.append(img_path + ".png")
    return image_paths