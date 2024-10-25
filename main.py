import os
import cv2
import torch

from ultralytics import YOLO
from utils.binary_to_jaso import jaso2char
from utils.jaso_complition import join_jamos

# 1. model load
# 모델이 저장된 경로 (여기서는 best.pt를 사용)
model_path = '/home2/kimmg/alpha/runs/detect/yolo_braille_hangeul_mkdata_only300e/weights/best.pt'
# model_path = YOUR_MODEL_PATH
model = YOLO(model_path)  # 학습된 YOLO 모델 불러오기

# 2. image input
def braille_to_text(image_path):
    image = cv2.imread(image_path)

    # 3. model output
    results = model(image)

    # 4. output(binary to jaso)
    # 예측 결과 
    # 바운딩 박스, confidence, 클래스
    # results[0].boxes.xyxy는 바운딩 박스 좌표, results[0].boxes.conf는 confidence score
    # results[0].boxes.cls는 클래스 예측
    boxes = results[0].boxes.xyxy.cpu().numpy()  # 바운딩 박스 좌표
    scores = results[0].boxes.conf.cpu().numpy()  # confidence score
    classes = results[0].boxes.cls.cpu().numpy()  # 클래스

    # 예측 결과 이미지 위에 표시
    binary_output = []
    for box, score, cls in zip(boxes, scores, classes):
        if score > 0.1:
            x1, y1, x2, y2 = map(int, box)
            label = f"{model.names[int(cls)]}: {score:.2f}"
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)  # 바운딩 박스 그리기
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            binary_output.append((x1, model.names[int(cls)]))


    binary = []

    binary_output.sort(key=lambda x:x[0]) # x1값을 기준으로 오름차순 sorting
    for _,b in binary_output:
        binary.append(b)



    #예측 결과 이미지 저장
    output_image_path = "/home2/kimmg/alpha/test_output/te.jpg"
    cv2.imwrite(output_image_path, image)

    # 5. jaso complition and print
    result = jaso2char(binary)
    print(result)
    combine_result = join_jamos(result)
    return combine_result

image_folder = "/home2/kimmg/alpha/dataset/testmk2datset/train/images"
folder = os.listdir("/home2/kimmg/alpha/dataset/testmk2datset/train/images")
a = []
for i in folder:
    image = image_folder+'/'+i
    a.append(braille_to_text(image))
for j in a:
    print(j)