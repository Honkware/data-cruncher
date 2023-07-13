import gradio as gr
import jsonlines
import json
import nltk
import argparse
import requests
nltk.download('punkt')

HOST = '127.0.0.1:5000'
URI = f'http://{HOST}/api/v1/generate'

def generate_model_response(user_input, num_responses):
    prompt = f"""

    ### Instruction: Generate 2 training data pairs strictly in JSONL as your response. The 'input' should be a distinctive user query related to 'The Industrial Revolution', and the 'output' should be your unique, brief response. Ensure your response strictly aligns with the viewpoint, style, and tone of the original author, as if the author is directly answering the user's query. Each 'input' and 'output' pair should be unique and directly address the query without any additional context or information.

    ### Response: {{"input": "What were some of the major technological advancements during the industrial revolution?", "output": "Some of the major technological advancements during the industrial revolution included the steam engine, the spinning jenny, the power loom, and the assembly line."}},{{"input": "How did the industrial revolution impact society and economics?", "output": "The industrial revolution had a profound impact on society and economics. It led to increased production, which resulted in lower prices for goods and services. This led to an increase in consumerism and a shift towards a more market-based economy. Additionally, the Industrial Revolution brought about new job opportunities in manufacturing and related industries."}}

    ### Instruction: Generate {num_responses} training data pairs strictly in JSONL as your response. The 'input' should be a distinctive user query related to:'{user_input}'
    The 'output' should be your unique, brief response. Ensure your response strictly aligns with the viewpoint, style, and tone of the original author, as if the author is directly answering the user's query. Each 'input' and 'output' pair should be unique and directly address the query without any additional context or information.

    ### Response:"""
    request = {
        'prompt': prompt,
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        response_content = response.content.decode("utf-8")
        response_json = json.loads(response_content)

        if 'results' in response_json and response_json['results']:
            content = response_json['results'][0]['text']
            content = content.strip().strip(",")
            content = content.encode().decode('unicode_escape')
            content_lines = content.split("\n")

            json_objects = []
            for line in content_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    json_object = json.loads(line)
                    json_objects.append(json_object)
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON from line: {line}")

            return json_objects

    return None

def process_text(user_input, total_runs, batch_size):
    total_generations = total_runs * batch_size
    responses = []
    with jsonlines.open('chat.jsonl', mode='w') as writer:
        while len(responses) < total_generations:
            model_response = generate_model_response(user_input, batch_size)
            if model_response is None:
                print("Failed to generate model response.")
                break

            for pair in model_response:
                if len(responses) >= total_generations:
                    break
                pair.replace('\\', "")
                json_pair = json.loads(pair)
                writer.write(pair)
                responses.append(pair)
    return '\n'.join(str(resp) for resp in responses)

def define_gradio_interface():
    return gr.Interface(
        fn=process_text,
        inputs=[
            gr.components.Textbox(label="User Input"),
            gr.components.Slider(minimum=1, maximum=1000, step=1, label="Total Runs"),
            gr.components.Slider(minimum=1, maximum=100, step=1, label="Batch Size"),
        ],
        outputs=gr.components.Textbox(label="Chat History"),
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true", help="generate a publicly shareable link")
    args = parser.parse_args()

    define_gradio_interface().launch(share=args.share)

if __name__ == "__main__":
    main()
