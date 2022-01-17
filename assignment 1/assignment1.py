"""
Objective
Extract text blocks from a PDF document with each paragraph as a separate line and text being in
reading order going from first column from top to bottom and then into second column and then
third column. Dump the output in an excel file.
The solution should be a general solution that can work on different pages of different PDFs.
Resources & Hints
PyMuPDF – PDF Parsing library
Identify columns by looking at the x coordinates difference
OpenCV can be used to combine lines using contours
Submission
Create a github repo, upload the code and the generated output excel along with requirements.txt
and share the link
"""

"""
Approach 1
"""


import pytesseract
import pandas as pd
import numpy as np
import fitz
import cv2
import csv
pdf = fitz.open("keppel-corporation-limited-annual-report-2018.pdf")
page = pdf.load_page(11)

remove_blocks = []
blocks = [x[4] for x in page.get_text("blocks")]
for i in range(len(blocks)):
    blocks[i] = blocks[i].strip()
    print(blocks[i])
    # each block can be removed if it is not necessary
    # enter 1 if the block is not required or else select 0
    # blocks that contain img reference or description of image can be removed
    remove = int(input("Remove block ? "))
    if (remove == 1):
        remove_blocks.append(i)


remove_blocks.reverse()
# removes unnesasary blocks
for i in remove_blocks:
    _ = blocks.pop(i)

new_blocks = []
remove_blocks = []
# merging 2 blocks that are part of a paragraph but are in 2 different columns
for i in range(len(blocks)-1):
    if (blocks[i][-1] != '.'):
        blocks[i] = blocks[i]+" "+blocks[i+1]
    new_block = blocks[i].replace('\n', '')
    new_blocks.append(new_block)


print(new_blocks)

pdf.close()
dict = {"": new_blocks}
df = pd.DataFrame(dict)
df.to_csv('A1.csv')

"""
Approach 2
"""

pix = page.get_pixmap()
pix.save('output.png')

image = cv2.imread('output.png')
base_image = image.copy()

# creating boxes
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
thresh = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 13))
dilate = cv2.dilate(thresh, kernal, iterations=1)
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

# pytesseact can be used to read text that are present in the boxes
results = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if h > 200 and w > 20:
        roi = image[y:y+h, x:x+h]
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)
        ocr_result = pytesseract.image_to_string(roi)
        ocr_result = ocr_result.split("\n")
        for item in ocr_result:
            results.append(item)

# answers are saved in results
cv2.imwrite("index_bbox_new.png", image)
