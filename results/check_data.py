import logging
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
    logging.info(f"{csv_file} used time: {time}s ≈ {round(time / 60, 2)}m")


def split_row(row):
    img = row['test_image']
    row['rotation'] = '_r' in img
    row['image'] = "_".join(img.split("_", 2)[:2]).replace('.jpeg', '')
    row['category'] = img.split("_", 2)[0]
    sigma = img.split("_")[-1].replace('.jpeg', '')
    if sigma in 'r':
        sigma = 'original'
    if len(img.split('_')) == 2:
        sigma = 'original'
    row['sigma'] = sigma

    return row


def csv_to_df(csv_file: str):
    df = pd.read_csv(csv_file)
    df['test_image'] = df['test_image'].apply(lambda img: img.split("/")[-1])
    df['proband'] = csv_file.split("_")[-1].replace('.csv', '')
    # example: portrait_4_r_4.jpeg -> portrait_4, True, 4
    done_df = df.apply(split_row, axis=1)
    #logging.info('\n' + done_df.head(20).to_string())
    return done_df


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    df_list = []
    for (_, _, filenames) in os.walk('./'):
        for filename in filenames:
            if filename.endswith('.csv'):
                check_number_img(filename)
                sum_resptime(filename)
                df_list.append(csv_to_df(filename))

    final_df = pd.concat(df_list, ignore_index=True)
#    final_df.drop(final_df.columns[0], axis=1, inplace=True)
    final_df.to_csv('result_final.csv', encoding='utf-8')
