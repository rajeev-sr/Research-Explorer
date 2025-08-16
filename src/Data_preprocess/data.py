from unstructured.partition.pdf import partition_pdf
from collections import defaultdict

def data_extracted(file):
    elements = partition_pdf(
        filename=file,
        strategy="hi_res",
        extract_images_in_pdf=True,
        extract_image_block_types=["Image", "Table"],
        extract_image_block_to_payload=False,
        extract_image_block_output_dir="extracted_data",
    )

    pages = defaultdict(list)

    for el in elements:
        page_num = el.metadata.page_number
        if page_num is None:
            continue

        if "unstructured.documents.elements.Table" in str(type(el)):
            # Add table image path before table content
            pages[page_num].append({
                "type": "table",
                "image_path": el.metadata.image_path,
                "content": str(el),
            })
        elif "unstructured.documents.elements.Image" in str(type(el)):
            pages[page_num].append({
                "type": "image",
                "image_path": el.metadata.image_path,
                "image_mime_type": el.metadata.image_mime_type
            })
        else:
            pages[page_num].append({
                "type": "text",
                "content": str(el)
            })

    # Format output for LLM: page-wise, preserving order and alignment
    formatted_pages = {}
    for page_num in sorted(pages.keys()):
        page_content = []
        for block in pages[page_num]:
            if block["type"] == "text":
                page_content.append(block["content"])
            elif block["type"] == "table":
                # Table image path before table content
                page_content.append(f"[TABLE_IMAGE_PATH]: {block['image_path']}")
                page_content.append(f"[TABLE]: {block['content']}")
            elif block["type"] == "image":
                page_content.append(f"[IMAGE_PATH]: {block['image_path']}")
        formatted_pages[page_num] = page_content

    return formatted_pages

# Example usage:
# pdf_data = data_extracted("/home/rajeev-kumar/Desktop/My_projects/Research-Explorer/data/12340120_EEP304_EXP1.pdf")
# print(pdf_data[2])  # Page 2 data

# data=data_extracted("/home/rajeev-kumar/Desktop/My_projects/Research-Explorer/data/12340120_EEP304_EXP1.pdf")
# print(data)