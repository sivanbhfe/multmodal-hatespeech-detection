import cv2
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def remove_text_ocr(input_path, output_path, resize_dim=(128, 128), lang="tam+eng"):
    custom_oem_psm_config = r'--oem 3 --psm 6'
    # Read image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError(f"Could not read {input_path}")

    # Run OCR to detect text bounding boxes
    data = pytesseract.image_to_data(img, config=custom_oem_psm_config, lang=lang, output_type=Output.DICT)

    # Create mask for text regions
    mask = img.copy()
    mask[:] = 0  # black mask

    n_boxes = len(data['level'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 30:  # only keep confident text detections
            (x, y, w, h) = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            pad = 5
            cv2.rectangle(mask, (x-pad, y-pad), (x + w + pad, y + h + pad), (255,255,255), -1)

    # Inpaint the detected text areas
    img_no_text = cv2.inpaint(img, cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY), 5, cv2.INPAINT_TELEA)

    # Resize to 128x128
    # img_resized = cv2.resize(img_no_text, resize_dim, interpolation=cv2.INTER_AREA)

    # Save result
    cv2.imwrite(output_path, img_no_text)
    print(f"✅ Saved cleaned image at {output_path}")

# Example usage
input_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\image\\Not_troll_1016.jpg"
output_file = "D:\\AI_Doctorate\\HateSpeechModel_Draft\\MultimodelHateSpeechDetection_related\\image\\Not_troll_1016_captionremoved.jpg"

remove_text_ocr(input_file, output_file, resize_dim=(128,128), lang="tam+eng")