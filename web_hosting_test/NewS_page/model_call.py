from .model_set import Summarize
def summary(content_text : str):
    summarize = Summarize('kykim/bertshared-kor-base', 'kykim/bertshared-kor-base')
    if content_text and len(content_text) > 512:
        content_text = content_text[:512]
    else:
        content_text = content_text[:len(content_text)]
    if len(content_text) > 30:
        result = summarize(content_text)
    else:
        result = content_text
    return result