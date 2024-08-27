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

    # print(f"Overlap: {num_overlap}\nIterations: {num_iterations}\nResponse_chars: {num_response_chars}\n")    
    system_prompt = f"Compress the following text in a way that you can reconstruct the intention of the human who wrote text as close as possible to the original intention. This is for yourself. It does not need to be human readable or understandable. Abuse of language mixing, abbreviations, symbols (unicode and emoji), or any other encodings or internal representations is all permissible, as long as it, if pasted in a new inference cycle, will yield near-identical results as the original text. Write only the compressed text, nothing else. Don't add text that is not necessary for you to understand the meaning of the original text. Your whole answer MUST respect the limit of {num_response_chars} characters."

    responses = []

    for i in range(num_iterations):
        if i == 0:
            num_start = 0
            num_end = int(num_chars + num_overlap)
        else:
            num_start = int(num_chars * i - num_overlap)
            num_end = int(num_chars * (i + 1) + num_overlap)

        prompt_text = extracted_text[num_start:num_end]
        response = call_endpoint(system_prompt, prompt_text)
        print(f"{int(((i + 1) / num_iterations) * 100)}%")
        responses.append(response)

    full_response = " ".join(responses)
    summary_system_prompt = "Please give a detailed overview of the following text, list the main points and answer in german."
    summary = call_endpoint(summary_system_prompt, full_response)
    print(f"\nSUMMARY:\n{summary}")

if __name__ == "__main__":
    main()