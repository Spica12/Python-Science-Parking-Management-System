import io
import cv2
import os
import base64
from django.utils import timezone
from pathlib import Path
from keras import saving
import numpy as np
from config.settings import BASE_DIR

class PlateRecognition:

    def __init__(self):
        # Визначення шляхів для завантаження ресурсів
        self.models_file_path = BASE_DIR / 'plate_recognition/models/'
        self.file_model = 'ua-license-plate-recognition-model-37x.h5'
        self.file_cascade = 'haarcascade_russian_plate_number.xml'
        self.full_path_models = os.path.join(self.models_file_path, self.file_model)
        self.full_path_cascade = os.path.join(self.models_file_path, self.file_cascade)

        # Завантаження моделі та каскадного класифікатора
        self.load_model()

    def load_model(self):
        # Завантаження моделі та каскадного класифікатора
        # Завантажує дані, необхідні для виявлення номерних знаків, з каскадного класифікатора.

        try:
            self.model = saving.load_model(self.full_path_models)
            self.plate_cascade = cv2.CascadeClassifier(self.full_path_cascade)
            self.model_load_status = True
        except Exception:
            self.model_load_status = None

    def predict_plate(self, file):
        # utc_datetime = timezone.now(tz=timezone.utc)
        file_image = file.read()

        uploaded_image = self.decode_io_file(file_image)

        output_image, num_image = self.extract_plate(uploaded_image)

        if num_image is not None:
            chars = self.segment_to_contours(num_image)
            predicted_str, total_accuracy = self.predict_result(chars, self.model)
            num_vehicle_str = str.replace(predicted_str, "#", "")

            num_result = {
                "num_vehicle_str": num_vehicle_str,
                "accuracy": total_accuracy,
                "num_img": num_image,
            }
        else:
            num_result = {}

        img = num_result.get('num_img', None)
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
            image = self.build_base64_image(io_buf.getvalue())
            num_result["num_img"] = image
            im_buf_arr = np.zeros(0)

            # tune output accuracy
            if not num_result["num_vehicle_str"]:
                num_result["accuracy"] = 0
            elif len(num_result["num_vehicle_str"]) < 6:
                num_result["accuracy"] *= 0.3

        else:
            num_result["num_img"] = None
            num_result["accuracy"] = 0
            print("num_result[num_img] = None")


        return num_result


    def decode_io_file(self, f):
        io_buf = io.BytesIO(f)
        # io_buf.seek(0)
        image_array = np.frombuffer(io_buf.getbuffer(), np.uint8)
        decode_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        return decode_img


    def extract_plate(self, image, text=""):

        plate_image = image.copy()
        roi = image.copy()
        plate = None
        # Виявляє номерні знаки та повертає координати та розміри контурів виявлених номерних знаків.
        plate_rect = self.plate_cascade.detectMultiScale(plate_image, scaleFactor = 1.05, minNeighbors = 8)

        width_max = 0 # використовується для сортування за шириною
        plate_max = None
        x_max = 0
        y_max = 0

        for (x, y, w, h) in plate_rect:

            # виконує пропорційне зміщення пікселів
            a, b = (int(0.1 * h), int(0.1 * w))
            aa, bb = (int(0.1 * h), int(0.1 * w))

            if h > 75: # пропускає розбиття за шириною високоякісного зображення
                b = 0
                bb = 0

            plate = roi[y+a : y+h-aa, x+b : x+w-bb, :]

            if width_max < w:
                plate_max = plate
                width_max = w
                x_max = x
                y_max = y

            # представлення виявлених контурів за допомогою малювання прямокутників навколо країв:
            cv2.rectangle(plate_image, (x+2,y), (x+w-3, y+h-5), (51,224,172), 3)
        if text != '':
            h = plate_max.shape[0]
            plate_image = cv2.putText(plate_image, text, (x_max, y_max-h//3),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL , 1.5, (51,224,172), 2, cv2.LINE_AA)

        return plate_image, plate_max

    def segment_to_contours(self, image, debug: bool = False):
        """
        Find characters in the resulting images
        """
        new_height = 75  # set fixed height
        # print("original plate[w,h]:", image.shape[1], image.shape[0], "new_shape:333,", new_height)

        # Preprocess cropped license plate image
        img_lp = cv2.resize(image, (333, new_height), interpolation=cv2.INTER_LINEAR_EXACT)

        img_gray_lp = cv2.cvtColor(img_lp, cv2.COLOR_BGR2GRAY)
        _, img_binary_lp = cv2.threshold(
            img_gray_lp, 112, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        LP_WIDTH = img_binary_lp.shape[1]
        LP_HEIGHT = img_binary_lp.shape[0]

        # Make borders white
        img_binary_lp[0:3, :] = 255
        img_binary_lp[:, 0:3] = 255
        img_binary_lp[new_height - 3 : new_height, :] = 255
        img_binary_lp[:, 330:333] = 255

        # Estimations of character contours sizes of cropped license plates
        dimensions = [LP_WIDTH / 24, LP_WIDTH / 8, LP_HEIGHT / 3, 2 * LP_HEIGHT / 3]
        # if debug:
        #     plt.imshow(img_binary_lp, cmap='gray')
        #     plt.title("original plate contour (binary)")
        #     plt.show()

        # Get contours within cropped license plate
        char_list = self. find_contours(dimensions, img_binary_lp)
        return char_list

    def find_contours(self, dimensions, img, debug=False):
        """
        Відповідність контурів номерному або символьному шаблону
        """
        i_width_threshold = 6

        # Знайдіть всі контури на зображенні
        cntrs, _ = cv2.findContours(img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Отримайте потенційні розміри
        lower_width = dimensions[0]
        upper_width = dimensions[1]
        lower_height = dimensions[2]
        upper_height = dimensions[3]

        # Перевірте найбільші 16 контурів на номерний або символьний шаблон
        cntrs = sorted(cntrs, key=cv2.contourArea, reverse=True)[:16]

        # бінарне зображення номерного знака на вхід: щоб перетворити img.shape(h,w) на img.shape(h,w,3)
        ii = np.dstack([img] * 3)

        x_cntr_list = []
        target_contours = []
        img_res = []
        for cntr in cntrs:
            # виявлення контуру на бінарному зображенні і повернення координат прямокутника, який його оточує
            intX, intY, intWidth, intHeight = cv2.boundingRect(cntr)

            # перевірка розмірів контуру для фільтрації символів за розміром контуру
            if (
                intWidth >= i_width_threshold
                and intWidth < upper_width
                and intHeight > lower_height
                and intHeight < upper_height
            ):
                x_cntr_list.append(
                    intX
                )  # stores the x coordinate of the character's contour, to used later for indexing the contours

                char_copy = np.zeros((44, 24))
                # видобуття кожного символу, використовуючи координати прямокутника, що його оточує.
                char = img[intY : intY + intHeight, intX : intX + intWidth]

                if intWidth >= i_width_threshold and intWidth < lower_width:
                    i_char = cv2.resize(
                        char, (intWidth, 42), interpolation=cv2.INTER_LINEAR_EXACT
                    )

                    char = np.full((42, 22), 255, dtype=np.uint8)
                    begin = int((22 - intWidth) / 2)  # center alignment
                    char[:, begin : begin + intWidth] = i_char[:, :]
                else:
                    char = cv2.resize(char, (22, 42), interpolation=cv2.INTER_LINEAR_EXACT)

                cv2.rectangle(
                    ii, (intX, intY), (intWidth + intX, intY + intHeight), (50, 21, 200), 2
                )
                # plt.imshow(ii, cmap='gray')

                # Make result formatted for classification: invert colors
                char = cv2.subtract(255, char)

                # Resize the image to 24x44 with black border
                char_copy[1:43, 1:23] = char
                char_copy[0:1, :] = 0
                char_copy[:, 0:1] = 0
                char_copy[43:44, :] = 0
                char_copy[:, 23:24] = 0

                img_res.append(
                    char_copy
                )  # List that stores the character's binary image (unsorted)
                if len(img_res) >= 10:
                    break

        # Return characters on ascending order with respect to the x-coordinate (most-left character first)
        # if debug:
        #     plt.show()
        # arbitrary function that stores sorted list of character indeces
        indices = sorted(range(len(x_cntr_list)), key=lambda k: x_cntr_list[k])
        img_res_copy = []
        for idx in indices:
            img_res_copy.append(
                img_res[idx]
            )  # stores character images according to their index
        img_res = np.array(img_res_copy)

        return img_res

    def predict_result(self, ch_contours, model):
        """
        # Predicting the output string number by contours
        """
        dic = {}
        characters = "#0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, c in enumerate(characters):
            dic[i] = c

        total_accuracy = 1.0

        output = []
        for i, ch in enumerate(ch_contours):
            img_ = cv2.resize(ch, (28, 28))  # interpolation=cv2.INTER_LINEAR by default

            img = self.fix_dimension(img_)
            img = img.reshape(1, 28, 28, 3)  # preparing image for the model

            prediction = model.predict(img, verbose=0)

            y_ = np.argmax(prediction, axis=-1)[0]  # predicting the class

            # print(y_, prediction.shape, prediction)
            character = dic[y_]
            # accuracy = prediction[0][y_]
            # print(f'{accuracy=}')
            # total_accuracy *= accuracy
            # print(f'{total_accuracy=}')

            output.append(character)

        plate_number = "".join(output)
        return plate_number, total_accuracy

    def fix_dimension(self, img):
        new_img = np.zeros((28, 28, 3))
        for i in range(3):
            new_img[:, :, i] = img
        return new_img

    def build_base64_image(self, binary_image_data):
        return base64.b64encode(binary_image_data).decode("utf-8")





image_plate_recognition = PlateRecognition()
