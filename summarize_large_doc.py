from configuration import load_config
from inference import call_endpoint
from pdf_text_extractor import extract_text

def main():
    file_path = "input.pdf"
    num_chars = 4000
    num_overlap_percentage = 0.1
    num_overlap = int(num_chars * num_overlap_percentage)

    extracted_text = extract_text(file_path)
    num_iterations = len(extracted_text) // num_chars
    num_response_chars = (num_chars + num_overlap) // num_iterations
    
    system_prompt = "You are a text compressor that is an expert in understanding complex texts. \
        Keeping the meaning and intention of the original text is your main concern. Wrap the \
        compressed text between [start] and [end] markers."

    prompt_template = "Compress the following text in a way that you can reconstruct the intention \
        of the human who wrote text as close as possible to the original intention. \
        This is for yourself. It does not need to be human readable or understandable. \
        Abuse of language mixing, abbreviations, symbols (unicode and emoji), \
        or any other encodings or internal representations is all permissible, as long \
        as it, if pasted in a new inference cycle, will yield near-identical results \
        as the original text. Write only the compressed text, nothing else. Don't add \
        text that is not necessary for you to understand the meaning of the original \
        text. Your whole answer MUST respect the limit of {num_response_chars} characters. \
        This is the text:\n `{chunk}`"

    responses = []

    for i in range(num_iterations):
        if i == 0:
            num_start = 0
            num_end = int(num_chars + num_overlap)
        else:
            num_start = int(num_chars * i - num_overlap)
            num_end = int(num_chars * (i + 1) + num_overlap)

        chunk = extracted_text[num_start:num_end]        
        prompt = prompt_template.format(num_response_chars=num_response_chars, chunk=chunk)
        response = call_endpoint(system_prompt, prompt)

        # Get text between [start] and [end] markers
        start_marker = "[start]"
        end_marker = "[end]"
        start_index = response.find(start_marker) + len(start_marker)
        end_index = response.find(end_marker)
        compressed_text_response = response[start_index:end_index]

        print(f"{int(((i + 1) / num_iterations) * 100)}%")
        responses.append(compressed_text_response)

    full_response = "\n---\n".join(responses)
    summary_system_prompt = "Please give an overview of the compressed text you get, list the main \
        points and group them by category. Answer in german."

    summary = call_endpoint(summary_system_prompt, full_response)
    print(f"\n{summary}")

if __name__ == "__main__":
    main()