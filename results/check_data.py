import logging
import numpy as np
import pandas as pd
import os


def check_number_img(csv_file: str):
    df = pd.read_csv('./../rating_experiments/design_rating_single.csv')
    design_img = df['test_image'].apply(lambda img: img.split("/")[-1])

    df = pd.read_csv(csv_file)
    result_img = df['test_image'].apply(lambda img: img.split("/")[-1])

    logging.info(f"{csv_file} #images: {design_img.equals(result_img)}")


def sum_resptime(csv_file: str):
    df = pd.read_csv(csv_file)
    time = round(df['resptime'].sum(), 2)
    logging.info(f"{csv_file} used time: {time}s ≈ {round(time/60, 2)}m")


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    for (_, _, filenames) in os.walk('./'):
        for filename in filenames:
            if filename.endswith('.csv'):
                check_number_img(filename)
                sum_resptime(filename)
