from google.cloud import vision
import os

_client = None
def _client_once():
    global _client
    if _client is None:
        # Check if credentials are properly configured
        if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
        
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not os.path.exists(credentials_path):
            raise FileNotFoundError(f"Google Cloud credentials file not found: {credentials_path}")
            
        _client = vision.ImageAnnotatorClient()
    return _client

def analyze_image(image_bytes: bytes):
    try:
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
        
    except Exception as e:
        # Return empty results instead of failing completely
        print(f"Vision API error: {e}")
        return {"logos": [], "text": "", "error": str(e)}
