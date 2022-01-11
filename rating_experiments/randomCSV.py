import os
import numpy as np

DIRECTORY = "./../img_out/final_20_12_7_4/"
MIN_DISTANCE = 3


def get_files(directory: str) -> list:
    l = []
    for f in os.listdir(directory):
        l.append(f)
    return l

def random_order(ims: list) -> list:
    new_order_ims = []

    last_images = []

    while len(ims) > 0:
        index = np.random.randint(0, len(ims))
        prefix = ims[index].replace(".", "_").split("_")
        prefix = prefix[0] + "_" + prefix[1]
        if not prefix in last_images:
            new_order_ims.append(ims[index])
            ims.pop(index)
            #keep up2date
            last_images.append(prefix)
            if len(last_images) > MIN_DISTANCE:
                last_images.pop(0)

    return new_order_ims


def write_to_csv(ims: list):
    f = open("design_rating_single.csv", "w")
    f.write("test_image\n")
    for im in ims:
        f.write(DIRECTORY + im + "\n")
    f.close()


if __name__ == '__main__':
    images = get_files(DIRECTORY)
    order = random_order(images)
    write_to_csv(order)

