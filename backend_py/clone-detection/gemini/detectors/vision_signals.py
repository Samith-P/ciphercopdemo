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

        # Comprehensive Vision AI analysis - extract maximum details
        print("Starting comprehensive Vision AI analysis...")
        
        # 1. Logo Detection
        logos_response = client.logo_detection(image=image)
        logos = logos_response.logo_annotations
        found_logos = []
        for logo in logos:
            logo_info = {
                "description": logo.description,
                "score": logo.score,
                "bounding_poly": {
                    "vertices": [{"x": v.x, "y": v.y} for v in logo.bounding_poly.vertices]
                } if logo.bounding_poly else None
            }
            found_logos.append(logo_info)
        
        # 2. Text Detection (OCR) - Full document text
        ocr_response = client.document_text_detection(image=image)
        full_text = ocr_response.full_text_annotation.text if ocr_response.full_text_annotation else ""
        
        # Extract text blocks with locations
        text_blocks = []
        if ocr_response.full_text_annotation:
            for page in ocr_response.full_text_annotation.pages:
                for block in page.blocks:
                    block_text = ""
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = "".join([symbol.text for symbol in word.symbols])
                            block_text += word_text + " "
                    if block_text.strip():
                        text_blocks.append({
                            "text": block_text.strip(),
                            "confidence": block.confidence if hasattr(block, 'confidence') else 0
                        })

        # 3. Web Detection - Find similar images and web entities
        web_response = client.web_detection(image=image)
        web_entities = []
        similar_images = []
        pages_with_matching_images = []
        
        if web_response.web_detection:
            # Web entities (what the image contains)
            for entity in web_response.web_detection.web_entities:
                if entity.description and entity.score > 0.5:  # Filter low-confidence entities
                    web_entities.append({
                        "description": entity.description,
                        "score": entity.score,
                        "entity_id": entity.entity_id if entity.entity_id else None
                    })
            
            # Similar images found on the web
            for image_match in web_response.web_detection.full_matching_images:
                similar_images.append({"url": image_match.url})
            
            # Pages with matching images
            for page in web_response.web_detection.pages_with_matching_images:
                page_info = {
                    "url": page.url,
                    "page_title": page.page_title if page.page_title else "",
                    "full_matching_images": [img.url for img in page.full_matching_images],
                    "partial_matching_images": [img.url for img in page.partial_matching_images]
                }
                pages_with_matching_images.append(page_info)

        # 4. Object Detection
        objects_response = client.object_localization(image=image)
        detected_objects = []
        for obj in objects_response.localized_object_annotations:
            obj_info = {
                "name": obj.name,
                "score": obj.score,
                "bounding_poly": {
                    "normalized_vertices": [{"x": v.x, "y": v.y} for v in obj.bounding_poly.normalized_vertices]
                } if obj.bounding_poly else None
            }
            detected_objects.append(obj_info)

        # 5. Face Detection (for detecting human elements)
        faces_response = client.face_detection(image=image)
        detected_faces = []
        for face in faces_response.face_annotations:
            face_info = {
                "detection_confidence": face.detection_confidence,
                "joy_likelihood": face.joy_likelihood.name if face.joy_likelihood else "UNKNOWN",
                "bounding_poly": {
                    "vertices": [{"x": v.x, "y": v.y} for v in face.bounding_poly.vertices]
                } if face.bounding_poly else None
            }
            detected_faces.append(face_info)

        # 6. Safe Search Detection
        safe_search_response = client.safe_search_detection(image=image)
        safe_search = {}
        if safe_search_response.safe_search_annotation:
            safe_search = {
                "adult": safe_search_response.safe_search_annotation.adult.name,
                "spoof": safe_search_response.safe_search_annotation.spoof.name,
                "medical": safe_search_response.safe_search_annotation.medical.name,
                "violence": safe_search_response.safe_search_annotation.violence.name,
                "racy": safe_search_response.safe_search_annotation.racy.name
            }

        # 7. Label Detection (general image classification)
        labels_response = client.label_detection(image=image)
        detected_labels = []
        for label in labels_response.label_annotations:
            if label.score > 0.6:  # Filter low-confidence labels
                detected_labels.append({
                    "description": label.description,
                    "score": label.score,
                    "topicality": label.topicality if hasattr(label, 'topicality') else 0
                })

        print(f"Vision AI analysis completed: {len(found_logos)} logos, {len(web_entities)} web entities, {len(detected_objects)} objects")

        return {
            "logos": found_logos,
            "text": full_text,
            "text_blocks": text_blocks,
            "web_entities": web_entities,
            "similar_images": similar_images,
            "pages_with_matching_images": pages_with_matching_images,
            "detected_objects": detected_objects,
            "detected_faces": detected_faces,
            "safe_search": safe_search,
            "labels": detected_labels
        }
        
    except Exception as e:
        # Return empty results instead of failing completely
        print(f"Vision API error: {e}")
        return {
            "logos": [], 
            "text": "", 
            "text_blocks": [],
            "web_entities": [],
            "similar_images": [],
            "pages_with_matching_images": [],
            "detected_objects": [],
            "detected_faces": [],
            "safe_search": {},
            "labels": [],
            "error": str(e)
        }
