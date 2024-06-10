# Medical-Chatbot-Using-LLM

## Steps To Run The Project

```bash
conda create -n medicalchatbot python=3.8 anaconda
```

```bash
conda activate medicalchatbot
```

```bash
pip install -r requirements.txtx
```

### Create a `.env` file in the root directory and add your Pinecone credentials as follows:

```ini
PINECONE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```


### Download the quantize model from the link provided in model folder & keep the model in the model directory:

```ini
## Download the Llama 2 Model:

llama-2-7b-chat.ggmlv3.q4_0.bin


## From the following link:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/tree/main
```


```bash
# run the following command to create folder structure
python templates.py
```