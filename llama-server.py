import logging
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
log_file = 'llama_server.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='a')

# Load model and tokenizer
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = "Llama-2-7b-chat-hf"
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float32, trust_remote_code=True).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

def generate_text(prompt, max_length=50):
    try:
        # Log the prompt
        logging.info(f"Received prompt: {prompt}")

        # Generate text using the model
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        inputs = inputs.to(device)
        outputs = model.generate(input_ids=inputs.input_ids, attention_mask=inputs.attention_mask, max_length=max_length)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Append an EOS token to the generated text
        generated_text += tokenizer.eos_token

        # Log the generated text
        logging.info(f"Generated text: {generated_text}")

        return generated_text
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": str(e)}

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Parse JSON request data
        request_data = request.json
        prompt = request_data.get("prompt")
        max_length = request_data.get("max_length", 50)

        # Generate text
        generated_text = generate_text(prompt, max_length)

        # Return JSON response
        return jsonify({"generated_text": generated_text})
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5002)
    print("Flask server is running at http://127.0.0.1:5000/")
