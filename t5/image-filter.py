#!/home/berada/.anaconda3/bin/python
import cv2 as cv
import numpy as np
import datetime
from math import ceil, floor, log10
from sys import argv


def psnr(img1, img2):
    pixel_dif = 0
    for row in range(0, img1.shape[0] - 1):
        for col in range(0, img1.shape[1] - 1):
            pixel_dif += (int(img1[row, col]) - int(img2[row, col])) ** 2
    mse = pixel_dif / (img1.shape[0] * img1.shape[1])
    return (10 * log10(255 ** 2 / mse))


def wiener(image, window_size, sigma_n):
    normalized = image / image.max()
    new_image = np.zeros(shape=normalized.shape)
    floor_value = floor(window_size / 2)
    ceil_value = ceil(window_size / 2)
    for row in range(ceil_value, normalized.shape[0] - floor_value):
        for col in range(ceil_value, normalized.shape[1] - floor_value):
            window = normalized[row - floor_value:row +
                                ceil_value, col - floor_value:col + ceil_value]
            micro_f = window.mean()
            sigma_f = window.var()
            sigma_s = min((sigma_f - sigma_n), 0)
            new_pixel = micro_f + \
                (sigma_s / (sigma_s + sigma_n)) * \
                (normalized[row, col] - micro_f)
            new_pixel = new_pixel * 255
            new_image[row, col] = new_pixel
    return new_image


def median(image, window_size):
    normalized = image / image.max()
    new_image = np.zeros(shape=normalized.shape)
    floor_value = floor(window_size / 2)
    ceil_value = ceil(window_size / 2)
    for row in range(ceil_value, normalized.shape[0] - floor_value):
        for col in range(ceil_value, normalized.shape[1] - floor_value):
            window = normalized[row - floor_value:row +
                                ceil_value, col - floor_value:col + ceil_value]
            new_pixel = np.median(window)
            new_pixel = new_pixel * 255
            new_image[row, col] = new_pixel
    return new_image


def usage():
    print('Modo de usar:')
    print('./filtro image_filename [wiener|median] [tamanho_da_janela]')
    print('tamanho_da_janela é um único inteiro ímpar (e.g. 3, 5, 7, etc)')


if __name__ == '__main__':
    init_time = datetime.datetime.now()
    if len(argv) != 4:
        usage()
        exit()
    file_name = argv[1]
    original_filename = file_name.split('_')[0] + '.png'
    operation = argv[2]
    size = int(argv[3])
    noisy_image = cv.imread(file_name, 0)
    original = cv.imread(original_filename, 0)
    print('PSNR imagem ruidosa: ' + str(psnr(original, noisy_image)))
    if operation == 'wiener':
        print('Utilizando filtro de Wiener com janela de ' +
              str(size) + 'x' + str(size))
        new_image = wiener(noisy_image, size, 0.01)
        output_filename = file_name.split(
            '.')[0] + 'wiener' + '_' + str(size) + 'x' + str(size) + '.png'
    elif operation == 'median':
        print('Utilizando filtro da Mediana com janela de ' +
              str(size) + 'x' + str(size))
        new_image = median(noisy_image, size)
        output_filename = file_name.split(
            '.')[0] + '_median' + '_' + str(size) + 'x' + str(size) + '.png'
    else:
        usage()
        exit()
    print('PSNR imagem filtrada: ' + str(psnr(original, new_image)))
    print('Tempo decorrido: ' + str(datetime.datetime.now() - init_time))
    cv.imwrite(output_filename, new_image)
