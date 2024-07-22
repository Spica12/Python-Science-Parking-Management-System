import os
import io
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import cv2
from keras.models import load_model

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

models_path = Path(__file__).resolve().parent.joinpath("models")

file_model = "ua-license-plate-recognition-model-37x.h5"
file_cascade = "haarcascade_russian_plate_number.xml"

full_path_models = "DS/models/ua-license-plate-recognition-model-37x.h5"
full_path_cascade = "DS/models/haarcascade_russian_plate_number.xml"

model = load_model(full_path_models)
plate_cascade = cv2.CascadeClassifier(full_path_cascade)

def resize_img(img, target_height=720):
    height, width = img.shape[:2]
    if height <= target_height:
        return img
    target_width = int(width * (target_height / height))
    resized_img = cv2.resize(img, (target_width, target_height))
    return resized_img

def extract_plate(img, plate_cascade, text=""):
    plate_img = img.copy()
    roi = img.copy()
    plate = None
    plate_rect = plate_cascade.detectMultiScale(plate_img, scaleFactor=1.05, minNeighbors=8)
    width_max = 0
    plate_max = None
    x_max = 0
    y_max = 0

    for x, y, w, h in plate_rect:
        a, b = (int(0.1 * h), int(0.1 * w))
        aa, bb = (int(0.1 * h), int(0.1 * w))

        if h > 75:
            b = 0
            bb = 0

        plate = roi[y + a : y + h - aa, x + b : x + w - bb, :]

        if width_max < w:
            plate_max = plate
            width_max = w
            x_max = x
            y_max = y

        cv2.rectangle(plate_img, (x + 2, y), (x + w - 3, y + h - 5), (51, 224, 172), 3)
    if text != "":
        h = plate_max.shape[0]
        plate_img = cv2.putText(
            plate_img,
            text,
            (x_max, y_max - h // 3),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            1.5,
            (51, 224, 172),
            2,
            cv2.LINE_AA,
        )

    return plate_img, plate_max

def find_contours(dimensions, img, debug=False):
    i_width_threshold = 6
    cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    lower_width = dimensions[0]
    upper_width = dimensions[1]
    lower_height = dimensions[2]
    upper_height = dimensions[3]
    cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:16]
    ii = np.dstack([img] * 3)
    x_cntr_list = []
    target_contours = []
    img_res = []

    for cntr in cntrs:
        intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

        if (
            intWidth >= i_width_threshold
            and intWidth < upper_width
            and intHeight > lower_height
            and intHeight < upper_height
        ):
            x_cntr_list.append(intX)
            char_copy = np.zeros((44, 24))
            char = img[intY : intY + intHeight, intX : intX + intWidth]

            if intWidth >= i_width_threshold and intWidth < lower_width:
                i_char = cv2.resize(
                    char, (intWidth, 42), interpolation=cv2.INTER_LINEAR_EXACT
                )

                char = np.full((42, 22), 255, dtype=np.uint8)
                begin = int((22 - intWidth) / 2)
                char[:, begin : begin + intWidth] = i_char[:, :]
            else:
                char = cv2.resize(char, (22, 42), interpolation=cv2.INTER_LINEAR_EXACT)

            cv2.rectangle(
                ii, (intX, intY), (intWidth + intX, intY + intHeight), (50, 21, 200), 2
            )
            char = cv2.subtract(255, char)
            char_copy[1:43, 1:23] = char
            char_copy[0:1, :] = 0
            char_copy[:, 0:1] = 0
            char_copy[43:44, :] = 0
            char_copy[:, 23:24] = 0

            img_res.append(char_copy)
            if len(img_res) >= 10:
                break

    if debug:
        plt.show()

    indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
    img_res_copy = []
    for idx in indices:
        img_res_copy.append(img_res[idx])
    img_res = np.array(img_res_copy)

    return img_res

def segment_to_contours(image, debug: bool = False):
    new_height = 75
    img_lp = cv2.resize(image, (333, new_height), interpolation=cv2.INTER_LINEAR_EXACT)
    img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
    _, img_binary_lp = cv2.threshold(img_gray_lp, 112, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    LP_WIDTH = img_binary_lp.shape[1]
    LP_HEIGHT = img_binary_lp.shape[0]
    img_binary_lp[0:3, :] = 255
    img_binary_lp[:, 0:3] = 255
    img_binary_lp[new_height - 3 : new_height, :] = 255
    img_binary_lp[:, 330:333] = 255
    dimensions = [LP_WIDTH / 24, LP_WIDTH / 8, LP_HEIGHT / 3, 2 * LP_HEIGHT / 3]
    char_list = find_contours(dimensions, img_binary_lp)
    return char_list

def fix_dimension(img):
    new_img = np.zeros((28, 28, 3))
    for i in range(3):
        new_img[:, :, i] = img
    return new_img

def predict_result(ch_contours, model):
    dic = {}
    characters = "#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, c in enumerate(characters):
        dic[i] = c

    total_accuracy = 1.0
    output = []

    for i, ch in enumerate(ch_contours):
        img_ = cv2.resize(ch, (28, 28))
        img = fix_dimension(img_)
        img = img.reshape(1, 28, 28, 3)
        prediction = model.predict(img, verbose=0)
        y_ = np.argmax(prediction, axis=-1)[0]
        character = dic[y_]
        output.append(character)

    plate_number = "".join(output)
    return plate_number, total_accuracy

def get_num_avto(img_avto):
    img = img_avto.copy()
    output_img, num_img = extract_plate(img, plate_cascade)
    if num_img is not None:
        chars = segment_to_contours(num_img)
        predicted_str, total_accuracy = predict_result(chars, model)
        num_avto_str = str.replace(predicted_str, "#", "")
        return {"num_avto_str": num_avto_str, "accuracy": total_accuracy, "num_img": num_img}
    else:
        return {}

def decode_io_file(f):
    io_buf = io.BytesIO(f)
    decode_img = cv2.imdecode(np.frombuffer(io_buf.getbuffer(), np.uint8), -1)
    return decode_img

def get_num_auto_png_io(f) -> dict:
    img = decode_io_file(f)
    return get_num_auto_png(img)

def get_num_auto_png(img) -> dict:
    num_result = get_num_avto(img)
    img = num_result.get("num_img", None)
    is_success = img is not None
    
    if is_success:
        try:
            is_success, im_buf_arr = cv2.imencode(
                ".png", img, params=[cv2.IMWRITE_PNG_COMPRESSION, 5]
            )
        except Exception:
            is_success = False

    if is_success:
        io_buf = io.BytesIO(im_buf_arr)
        num_result["num_img"] = io_buf.getvalue()
        im_buf_arr = np.zeros(0)
        if not num_result["num_avto_str"]:
            num_result["accuracy"] = 0
        elif len(num_result["num_avto_str"]) < 6:
            num_result["accuracy"] *= 0.3
    else:
        num_result["num_img"] = None
        num_result["accuracy"] = 0
        print("num_result[num_img] = None")

    return num_result
