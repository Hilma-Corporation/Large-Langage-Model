import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()


def openai_translate_text(api_key, text, source_lang, target_lang, model="gpt-4", temperature=0.7, max_tokens=100, stop=None):
    """
    Translates a given text from source language to target language using the OpenAI API.

    Parameters:
    api_key (str): The API key for accessing the OpenAI API.
    text (str): The text to be translated.
    source_lang (str): The source language of the text.
    target_lang (str): The target language for the translation.
    model (str): The model to use for translation (default is "gpt-4").
    temperature (float): Sampling temperature to control the creativity of the model (default is 0.7).
    max_tokens (int): The maximum number of tokens in the generated translation (default is 100).
    stop (str or list): Optional stop sequence to end the generation.

    Returns:
    str: Translated text generated by the OpenAI API.
    """
    task_description = f"Translate the following text from {source_lang} to {target_lang}."

    prompt_content = f"""
    {task_description}

    Text: {text}
    Translation:
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt_content}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stop": stop
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        translated_text = response_json["choices"][0]["message"]["content"].strip()
        return translated_text
    else:
        return f"Error {response.status_code}: {response.text}"



def anthropic_translate_text(api_key, text, source_language, target_language, model="claude-3-5-sonnet-20240620", max_tokens=1024, temperature=0.7):
    """
    Translates a given text from a source language to a target language using the Anthropic API.

    Parameters:
    api_key (str): The API key for accessing the Anthropic API.
    text (str): The text to be translated.
    source_language (str): The source language of the text.
    target_language (str): The target language for the translation.
    model (str): The model to use for text generation (default is "claude-3-5-sonnet-20240620").
    max_tokens (int): The maximum number of tokens in the generated response (default is 1024).
    temperature (float): Sampling temperature to control the creativity of the model (default is 0.7).

    Returns:
    str: Translation generated by the Anthropic API.
    """
    url = "https://api.anthropic.com/v1/messages"
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": f"Please translate the following text from {source_language} to {target_language}:\n\n{text}"}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        translated_text = response_json["content"][0]["text"].strip()
        return translated_text
    else:
        return f"Error {response.status_code}: {response.text}"



def run_mistral(api_key, user_message, model="mistral-medium-latest"):
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 512,
        "stream": False,
        "safe_prompt": False,
        "random_seed": 1337
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"


def mistral_translate_text(api_key, text, source_lang, target_lang, model="mistral-medium-latest"):
    """
    Translates a given text from source language to target language using the Mistral API.

    Parameters:
    api_key (str): The API key for accessing the Mistral API.
    text (str): The text to be translated.
    source_lang (str): The source language of the text.
    target_lang (str): The target language for the translation.
    model (str): The model to use for text generation (default is "mistral-medium-latest").

    Returns:
    str: Translated text generated by the Mistral API.
    """
    user_message = f"Translate the following text from {source_lang} to {target_lang}:\n\n{text}"
    return run_mistral(api_key, user_message, model=model)

# Exemple d'utilisation
if __name__ == "__main__":
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is not set.")
  
