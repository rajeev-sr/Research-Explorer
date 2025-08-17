from explain import explain_booklet
from diagram_render import render_diagrams
from pdf_formation import booklet_to_pdf

pdf_path = "/home/rajeev-kumar/Desktop/My_projects/Research-Explorer/data/1706.03762v7.pdf"
hf_token = "hf token"  # Your HuggingFace token if needed

booklet, diagrams = explain_booklet(pdf_path, hf_token=hf_token)
image_paths = render_diagrams(diagrams, "diagrams")
booklet_to_pdf(booklet, image_paths, "booklet_output.pdf")