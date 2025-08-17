from transformers import pipeline
from data import data_extracted

def chunk_content(all_content, max_tokens=3500):
    chunks = []
    current_chunk = []
    current_length = 0
    for block in all_content:
        block_length = len(block.split())
        if current_length + block_length > max_tokens:
            chunks.append("\n".join(current_chunk))
            current_chunk = [block]
            current_length = block_length
        else:
            current_chunk.append(block)
            current_length += block_length
    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks

def explain_booklet(file_path, model_name="mistralai/Mistral-7B-Instruct-v0.2", hf_token=None):
    page_data_dict = data_extracted(file_path)
    all_content = []
    for page_num in sorted(page_data_dict.keys()):
        all_content.extend(page_data_dict[page_num])
    chunks = chunk_content(all_content)

    generator = pipeline(
        "text-generation",
        model=model_name,
        max_new_tokens=2048,
        token=hf_token
    )

    booklet_sections = []
    diagram_codes = []

    for i, chunk in enumerate(chunks):
        prompt = (
            "You are creating a student-friendly booklet explaining a research paper.\n"
            "- Explain the concepts, context, and methods in simple terms.\n"
            "- Organize the booklet with sections, headings, and logical flow.\n"
            "- If possible, generate a Graphviz DOT code for a flowchart or concept map explaining the main method or process. Mark it as [DIAGRAM]: ...\n"
            "- Format output for PDF readability (use headings, bullet points, numbered lists, etc.).\n"
            f"Content:\n{chunk}\n"
        )
        result = generator(prompt)[0]['generated_text']
        booklet_sections.append(result)

        # Extract Graphviz code for diagrams
        import re
        diagram_matches = re.findall(r"\[DIAGRAM\]:(.*?)```", result, re.DOTALL)
        diagram_codes.extend([code.strip() for code in diagram_matches])

    booklet_text = "\n\n".join(booklet_sections)
    return booklet_text, diagram_codes