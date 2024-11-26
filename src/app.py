import os
import cv2
from lib.filters import get_grayscale, thresholding, pytesseract
from lib.format_output import format_output
import matplotlib.pyplot as plt


def apply_filter(plate):
    gray = get_grayscale(plate)
    thresh = thresholding(gray)
    return thresh


def scan_plate(image):
    plt.imshow(image)
    plt.show()
    custom_config = r'-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- --psm 6'
    plate_number = (pytesseract.image_to_string(image, config=custom_config))
    print(plate_number.strip())
    return plate_number.strip()


def validate_plate(plate_number, authorized_plate):
    if plate_number in authorized_plate:
        return 'AUTHORIZED'
    else:
        return 'NOT AUTHORIZED'


def main():
    authorized_plate = ['FUN-0972', 'BRA2E19']

    # Caminho absoluto para a pasta de imagens
    image_dir = r'C:\Users\T-Gamer\Documents\GitHub\CarPlate-Recognition\images'

    # Verifica se a pasta existe
    if not os.path.exists(image_dir):
        print(f"Erro: A pasta '{image_dir}' não existe.")
        return

    # Lista os arquivos na pasta
    filenames = os.listdir(image_dir)
    if not filenames:
        print(f"Erro: A pasta '{image_dir}' está vazia.")
        return

    # Caminhos completos para as imagens
    images = [os.path.join(image_dir, file) for file in filenames]

    plates = []
    plates_filter_applied = []
    plates_numbers = []
    data = []
    

    # Append the files name to list data
    for i in range(len(filenames)):
        data.append([])
        data[i].append(filenames[i])

    # Make an append to list plates
    for i in images:
        plates.append(cv2.imread(i))

    # Calls the function apply_filter() passing the plate image
    for i in range(len(plates)):
        plates_filter_applied.append(apply_filter(plates[i]))

    # Calls the function scan_plate() passing the plate image with filter applied
    for i in range(len(plates_filter_applied)):
        plates_numbers.append(scan_plate(plates_filter_applied[i]))
        data[i].append(plates_numbers[i])

    # Calls the function validate_plate() passing the plate number
    for i in range(len(plates_numbers)):
        data[i].append(validate_plate(plates_numbers[i], authorized_plate))

    format_output(data)


if __name__ == "__main__":
    main()
