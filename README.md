# Data Cruncher

Data Cruncher is a tool that utilizes OpenAI's GPT-3.5-turbo-16k model or Oobabooga's text-generation-webui to generate training data pairs.

## Setup

To set up and run the tool, follow these steps:

1. Install the required dependencies by running the following command:
```
pip install -r requirements.txt
```
2. Run the tool using one of the following methods:

- If you have access to the OpenAI API, use the following command:

  ```
  python gen_openai.py
  ```

- If you want to use the Oobabooga Text Gen web UI, use the following command:

  ```
  python gen_local.py
  ```

3. Additionally, if you want to generate a publicly shareable link, use the `--share` argument with the command (if applicable).
```
python gen_local.py --share
```