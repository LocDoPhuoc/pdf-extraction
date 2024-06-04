import os
import numpy as np
import cv2
from paddleocr import PPStructure,draw_structure_result,save_structure_res
import fitz
from PIL import Image

ocr_engine = PPStructure(show_log=True, ocr=True, structure_version='PP-StructureV2', lang='en')

save_folder = 'paddle_output'
img_path = 'pdfs/3004529162.pdf'
# img = cv2.imread(img_path)
# result = table_engine(img)
# save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

imgs = []
with fitz.open(img_path) as pdf:
    for pg in range(0, pdf.page_count):
        page = pdf[pg]
        mat = fitz.Matrix(2, 2)
        pm = page.get_pixmap(matrix=mat, alpha=False)

        # if width or height > 2000 pixels, don't enlarge the image
        if pm.width > 2000 or pm.height > 2000:
            pm = page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False)

        img = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        imgs.append(img)

for index, img in enumerate(imgs):
    result = ocr_engine(img)
    save_structure_res(result, save_folder, os.path.basename(img_path).split('.')[0], index)
    for line in result:
        line.pop('img')
        print(line)