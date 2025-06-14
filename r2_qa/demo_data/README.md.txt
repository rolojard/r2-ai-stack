# r2_qa Package

**Adds “Ask R2” functionality** using a local Star Wars knowledge base and LLM + TTS.

## Files

- `knowledge_base.py` — builds/loads FAISS index of wiki passages  
- `demo_data/sample_passages.json` — small sample of SW facts  
- `qa_module.py` — retrieves passages, calls OpenAI (or stub)  
- `tts_driver.py` — generates speech via gTTS + plays via SoundDriver  
- `requirements.txt`          

## Setup

```bash
pip install -r r2_qa/requirements.txt
