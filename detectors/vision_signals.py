from google.cloud import vision

_client = None
def _client_once():
    global _client
    if _client is None:
        _client = vision.ImageAnnotatorClient()
    return _client

def analyze_image(image_bytes: bytes):
    client = _client_once()
    image = vision.Image(content=image_bytes)

    logos = client.logo_detection(image=image).logo_annotations
    ocr = client.document_text_detection(image=image)

    found_logos = [
        {"description": l.description, "score": l.score}
        for l in logos if l.description
    ]
    text = ocr.full_text_annotation.text if ocr.full_text_annotation else ""

    return {"logos": found_logos, "text": text}
