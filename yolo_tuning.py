import os
import cv2
import torch
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
data_yaml = "dataset/testmk2datset/data.yaml"

results = model.train(
    data=data_yaml,          # 데이터셋 경로 및 설정이 담긴 YAML 파일 경로
    epochs=500,               # 학습 횟수 (epochs)
    imgsz=640,               # 이미지 크기 (YOLO에서 추천하는 기본 크기)
    batch=1,                # 배치 크기
    workers=4,               # 데이터 로딩에 사용할 CPU 코어 수
    device=0,     
    lr0=0.001,
    lrf=0.2,         
    name="yolo_braille_hangeul_mkdata_only500e"  # 학습 결과 저장 폴더 이름
)
