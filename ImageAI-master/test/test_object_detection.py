import os, sys
from typing import List
import shutil
import cv2
import uuid
from PIL import Image
import numpy as np
import pytest
from os.path import dirname
sys.path.insert(1, os.path.join(dirname(dirname(os.path.abspath(__file__)))))
from imageai.Detection import ObjectDetection

test_folder = dirname(os.path.abspath(__file__))


def delete_cache(paths: List[str]):
    for path in paths:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


@pytest.mark.parametrize(
    "input_image, output_type, extract_objects",
    [
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "4.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", True),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", False),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", True),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", True),
    ]
)
def test_object_detection_retinanet(input_image, output_type, extract_objects):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(test_folder, "data-models", "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
    detector.loadModel()

    output_img_path = os.path.join(test_folder, "data-images", str(uuid.uuid4()) + ".jpg")

    if output_type == "array":
        if extract_objects:
            output_image_array, detections, extracted_objects = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type, extract_detected_objects=extract_objects)

            assert len(extracted_objects) > 1
            for extracted_obj in extracted_objects:
                assert type(extracted_obj) == np.ndarray
            assert type(detections) == list
        else:
            output_image_array, detections = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type)
            assert type(output_image_array) == np.ndarray
            assert type(detections) == list
    else:
        if extract_objects:
            detections, extracted_object_paths = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path, extract_detected_objects=True)

            assert type(detections) == list
            assert os.path.isfile(output_img_path)
            assert len(extracted_object_paths) > 3
            delete_cache(
                extracted_object_paths
            )
            delete_cache(
                [extracted_object_paths[0], output_img_path]
            )
        else:
            detections = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path)
            assert type(detections) == list
            delete_cache(
                [output_img_path]
            )
    

    for eachObject in detections:
        assert type(eachObject) == dict
        assert "name" in eachObject.keys()
        assert type(eachObject["name"]) == str 
        assert "percentage_probability" in eachObject.keys()
        assert type(eachObject["percentage_probability"]) == float
        assert "box_points" in eachObject.keys()
        assert type(eachObject["box_points"]) == list
        box_points = eachObject["box_points"]
        for point in box_points:
            assert type(point) == int
        assert box_points[0] < box_points[2]
        assert box_points[1] < box_points[3]


@pytest.mark.parametrize(
    "input_image, output_type, extract_objects",
    [
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "4.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", True),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", False),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", True),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", True),
    ]
)
def test_object_detection_yolov3(input_image, output_type, extract_objects):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(test_folder, "data-models", "yolov3.pt"))
    detector.loadModel()

    output_img_path = os.path.join(test_folder, "data-images", str(uuid.uuid4()) + ".jpg")

    if output_type == "array":
        if extract_objects:
            output_image_array, detections, extracted_objects = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type, extract_detected_objects=extract_objects)

            assert len(extracted_objects) > 1
            assert type(detections) == list
            for extracted_obj in extracted_objects:
                assert type(extracted_obj) == np.ndarray
        else:
            output_image_array, detections = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type)
            assert type(output_image_array) == np.ndarray
            assert type(detections) == list
    else:
        if extract_objects:
            detections, extracted_object_paths = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path, extract_detected_objects=True)

            assert os.path.isfile(output_img_path)
            assert len(extracted_object_paths) > 3
            assert type(detections) == list
            delete_cache(
                extracted_object_paths
            )
            delete_cache(
                [extracted_object_paths[0], output_img_path]
            )
        else:
            detections = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path)
            assert type(detections) == list
            delete_cache(
                [output_img_path]
            )

    

    for eachObject in detections:
        assert type(eachObject) == dict
        assert "name" in eachObject.keys()
        assert type(eachObject["name"]) == str 
        assert "percentage_probability" in eachObject.keys()
        assert type(eachObject["percentage_probability"]) == float
        assert "box_points" in eachObject.keys()
        assert type(eachObject["box_points"]) == list
        box_points = eachObject["box_points"]
        for point in box_points:
            assert type(point) == int
        assert box_points[0] < box_points[2]
        assert box_points[1] < box_points[3]


@pytest.mark.parametrize(
    "input_image, output_type, extract_objects",
    [
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "4.jpg"), "file", False),
        (os.path.join(test_folder, test_folder, "data-images", "1.jpg"), "file", True),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", False),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "1.jpg")), "array", True),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "11.jpg")), "array", True),
    ]
)
def test_object_detection_tiny_yolov3(input_image, output_type, extract_objects):
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(os.path.join(test_folder, "data-models", "tiny-yolov3.pt"))
    detector.loadModel()


    output_img_path = os.path.join(test_folder, "data-images", str(uuid.uuid4()) + ".jpg")

    if output_type == "array":
        if extract_objects:
            output_image_array, detections, extracted_objects = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type, extract_detected_objects=extract_objects)

            assert len(extracted_objects) > 1
            assert type(detections) == list
            for extracted_obj in extracted_objects:
                assert type(extracted_obj) == np.ndarray
        else:
            output_image_array, detections = detector.detectObjectsFromImage(input_image=input_image, output_type=output_type)
            assert type(output_image_array) == np.ndarray
            assert type(detections) == list
    else:
        if extract_objects:
            detections, extracted_object_paths = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path, extract_detected_objects=True)

            assert os.path.isfile(output_img_path)
            assert len(extracted_object_paths) > 1
            assert type(detections) == list
            delete_cache(
                extracted_object_paths
            )
            delete_cache(
                [extracted_object_paths[0], output_img_path]
            )

        else:
            detections = detector.detectObjectsFromImage(input_image=input_image, output_image_path=output_img_path)
            assert type(detections) == list
            delete_cache(
                [output_img_path]
            )
        
    

    for eachObject in detections:
        assert type(eachObject) == dict
        assert "name" in eachObject.keys()
        assert type(eachObject["name"]) == str 
        assert "percentage_probability" in eachObject.keys()
        assert type(eachObject["percentage_probability"]) == float
        assert "box_points" in eachObject.keys()
        assert type(eachObject["box_points"]) == list
        box_points = eachObject["box_points"]
        for point in box_points:
            assert type(point) == int
        assert box_points[0] < box_points[2]
        assert box_points[1] < box_points[3]


@pytest.mark.parametrize(
    "input_image",
    [
        (os.path.join(test_folder, test_folder, "data-images", "11.jpg")),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
    ]
)
def test_object_detection_retinanet_custom_objects(input_image):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(os.path.join(test_folder, "data-models", "retinanet_resnet50_fpn_coco-eeacb38b.pth"))
    detector.loadModel()

    custom = detector.CustomObjects(person=True, cell_phone=True)

    custom_detections = detector.detectObjectsFromImage(input_image=input_image, custom_objects=custom)
    
    for custom_detection in custom_detections:
        assert custom_detection["name"] in ["person", "cell phone"]

    detections = detector.detectObjectsFromImage(input_image=input_image)

    assert len(detections) > len(custom_detections)


@pytest.mark.parametrize(
    "input_image",
    [
        (os.path.join(test_folder, test_folder, "data-images", "11.jpg")),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
    ]
)
def test_object_detection_yolov3_custom_objects(input_image):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(test_folder, "data-models", "yolov3.pt"))
    detector.loadModel()

    custom = detector.CustomObjects(person=True, cell_phone=True)

    custom_detections = detector.detectObjectsFromImage(input_image=input_image, custom_objects=custom)
    
    for custom_detection in custom_detections:
        assert custom_detection["name"] in ["person", "cell phone"]

    detections = detector.detectObjectsFromImage(input_image=input_image)

    assert len(detections) > len(custom_detections)


@pytest.mark.parametrize(
    "input_image",
    [
        (os.path.join(test_folder, test_folder, "data-images", "11.jpg")),
        (cv2.imread(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
        (Image.open(os.path.join(test_folder, test_folder, "data-images", "11.jpg"))),
    ]
)
def test_object_detection_tiny_yolov3_custom_objects(input_image):
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(os.path.join(test_folder, "data-models", "tiny-yolov3.pt"))
    detector.loadModel()

    custom = detector.CustomObjects(person=True, cell_phone=True)

    custom_detections = detector.detectObjectsFromImage(input_image=input_image, custom_objects=custom)
    
    for custom_detection in custom_detections:
        assert custom_detection["name"] in ["person", "cell phone"]

    detections = detector.detectObjectsFromImage(input_image=input_image)

    assert len(detections) > len(custom_detections)

