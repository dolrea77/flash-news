from transformers import BertTokenizerFast
from transformers import EncoderDecoderModel
class Summarize():
    def __init__(self, model_name:str, tokenizer_name:str):
        self.model = EncoderDecoderModel.from_pretrained(model_name)
        self.tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name)
    def __call__(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors= 'pt')
        sentence_length = len(input_ids[0])
        min_length = max(10, int(0.1*sentence_length))
        max_length = min(128, int(0.3*sentence_length))
        outputs = self.model.generate(
            input_ids,
            min_length=min_length,
            max_length=max_length
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)