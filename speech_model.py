import os
import librosa
import torch
from transformers import (
    Wav2Vec2ProcessorWithLM,
    Wav2Vec2Processor, 
    Wav2Vec2ForCTC
)
from tqdm import tqdm
# torch.multiprocessing.set_start_method("spawn",force=True) 


class Model:
  def __init__(self,model,processor,LM=False,device="cpu"):
    print("Loading model...")
    self.device = device
    self.model = Wav2Vec2ForCTC.from_pretrained(model,revision="413f0f2fb9aaf2a203ea7b0b2ea5613c29417fb6").to(self.device)
    self.LM = LM
    if self.LM:
      self.processor = Wav2Vec2ProcessorWithLM.from_pretrained(processor)
    else:
      self.processor = Wav2Vec2Processor.from_pretrained(processor)
  
  def transcribe(self, paths):
        sampling_rate = self.processor.feature_extractor.sampling_rate
        result = []
        for path in tqdm(paths):
            waveforms = librosa.load(path, sampling_rate)
            inputs = self.processor(waveforms[0], sampling_rate=sampling_rate, return_tensors="pt", padding=True, do_normalize=True)
            with torch.no_grad():
                if hasattr(inputs, "attention_mask"):
                    logits = self.model(inputs.input_values.to(self.device),attention_mask=inputs.attention_mask.to(self.device)).logits
                else:
                    logits = self.model(inputs.input_values.to(self.device)).logits
            if self.LM:
              result += self.processor.batch_decode(logits.cpu().numpy()).text
            else:
              result += self.processor.batch_decode(torch.argmax(logits, dim=-1))

        return result

