from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image
import spacy

nlp = spacy.load("en_core_med7_lg")

def load_model():
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    # Download the YOLOv9 model
    model_path = hf_hub_download(repo_id="Riksarkivet/yolov9-lines-within-regions-1", filename="model.pt")
    print("Model downloaded to:", model_path)

    # Load the model
    yolo_model = YOLO(model_path)
    print("Model loaded successfully!")

    return processor, model, yolo_model


def segment_text_lines(image):
    if not isinstance(image, np.ndarray):
        image_np = np.array(image.convert('RGB'))
    else:
        image_np = image
    
    _, _, yolo_model = load_model()

    results = yolo_model(image_np)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    boxes = sorted(boxes, key=lambda b: b[1])
    image_with_boxes = image_np.copy()
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

    segmented_image = Image.fromarray(image_with_boxes)
    
    return segmented_image

def segment_extract_text(image):
    if not isinstance(image, np.ndarray):
        image_np = np.array(image.convert('RGB'))
    else:
        image_np = image
    
    processor, model, yolo_model = load_model()
    results = yolo_model(image_np)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    boxes = sorted(boxes, key=lambda b: b[1])
    extracted_text = []
    image_with_boxes = image_np.copy()
    for box in boxes:
        x_min, y_min, x_max, y_max = map(int, box)
        line_crop = image_np[y_min:y_max, x_min:x_max]
        pil_crop = Image.fromarray(line_crop)
        #Perform HTR
        pixel_values = processor(pil_crop, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        extracted_text.append(text)
        #Draw bounding box on image
        cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
    all_text= ""
    for i, text in enumerate(extracted_text):
        all_text += text + " "    
    return all_text,Image.fromarray(image_with_boxes)




import spacy
import re
from flask import Flask, request, jsonify
nlp = spacy.load("en_core_med7_lg")
known_terms = {"drug", "tab", "mg" , "gm" , "g"}

def enhance_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    words = cleaned_text.split()
    filtered_words = [
        word for word in words 
        if len(word) > 3 or word.lower() in known_terms
    ]
    
    enhanced_text = " ".join(filtered_words)

    return enhanced_text

def extract_drugs_and_dosages(text):

    cleaned_text = enhance_text(text)
    doc = nlp(cleaned_text)
    medications = []
    current_med = {"drug": None, "dosage": None}
    for ent in doc.ents:
        if ent.label_ == "DRUG":
            if current_med["drug"]:
                medications.append(current_med)
            current_med = {"drug": ent.text, "dosage": None} 

        elif ent.label_ == "STRENGTH":
            current_med["dosage"] = ent.text

    if current_med["drug"]:
        medications.append(current_med)
    return medications



#chatgpt code
# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
# from huggingface_hub import hf_hub_download
# from ultralytics import YOLO
# import numpy as np
# import cv2
# from PIL import Image
# import spacy
# import re

# # ✅ حمّل كل حاجة مرة واحدة بس
# print("Loading models...")

# processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
# model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')
# yolo_model_path = hf_hub_download(repo_id="Riksarkivet/yolov9-lines-within-regions-1", filename="model.pt")
# yolo_model = YOLO(yolo_model_path)
# nlp = spacy.load("en_core_med7_lg")

# print("All models loaded successfully!")

# # ✅ كلمات معروفة للحفاظ على معناها
# known_terms = {"drug", "tab", "mg", "gm", "g"}


# # ---------------------------------------------------------
# # 🔹 Segmentation Only (Boxes on text lines)
# # ---------------------------------------------------------
# def segment_text_lines(image):
#     if not isinstance(image, np.ndarray):
#         image_np = np.array(image.convert('RGB'))
#     else:
#         image_np = image

#     results = yolo_model(image_np)
#     boxes = results[0].boxes.xyxy.cpu().numpy()
#     boxes = sorted(boxes, key=lambda b: b[1])

#     image_with_boxes = image_np.copy()
#     for box in boxes:
#         x_min, y_min, x_max, y_max = map(int, box)
#         cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

#     return Image.fromarray(image_with_boxes)


# # ---------------------------------------------------------
# # 🔹 Full Text Extraction (Text + Segmented Image)
# # ---------------------------------------------------------
# def segment_extract_text(image):
#     if not isinstance(image, np.ndarray):
#         image_np = np.array(image.convert('RGB'))
#     else:
#         image_np = image

#     results = yolo_model(image_np)
#     boxes = results[0].boxes.xyxy.cpu().numpy()
#     boxes = sorted(boxes, key=lambda b: b[1])

#     extracted_text = []
#     image_with_boxes = image_np.copy()

#     for box in boxes:
#         x_min, y_min, x_max, y_max = map(int, box)
#         line_crop = image_np[y_min:y_max, x_min:x_max]
#         pil_crop = Image.fromarray(line_crop)

#         pixel_values = processor(pil_crop, return_tensors="pt").pixel_values
#         generated_ids = model.generate(pixel_values)
#         text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
#         extracted_text.append(text)

#         cv2.rectangle(image_with_boxes, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

#     all_text = " ".join(extracted_text)
#     return all_text, Image.fromarray(image_with_boxes)


# # ---------------------------------------------------------
# # 🔹 Clean & Enhance text
# # ---------------------------------------------------------
# def enhance_text(text):
#     cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
#     words = cleaned_text.split()
#     filtered_words = [
#         word for word in words
#         if len(word) > 3 or word.lower() in known_terms
#     ]
#     return " ".join(filtered_words)


# # ---------------------------------------------------------
# # 🔹 Extract Drugs & Dosages
# # ---------------------------------------------------------
# def extract_drugs_and_dosages(text):
#     cleaned_text = enhance_text(text)
#     doc = nlp(cleaned_text)

#     medications = []
#     current_med = {"drug": None, "dosage": None}

#     for ent in doc.ents:
#         if ent.label_ == "DRUG":
#             if current_med["drug"]:
#                 medications.append(current_med)
#             current_med = {"drug": ent.text, "dosage": None}
#         elif ent.label_ == "STRENGTH":
#             current_med["dosage"] = ent.text

#     if current_med["drug"]:
#         medications.append(current_med)

#     return medications
