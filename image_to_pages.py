import argparse
import sys

import numpy as np
from PIL import Image


def main(args):
    """
    Crops input image to square and makes foldable bookmark

    Args:
        args (argparse.Namespace): Arguments from argparse
    """
    img_path = args.picture
    img = Image.open(img_path)

    # get minimum size axis and crop
    min_size = min(img.size)
    img = img.crop([0, 0, min_size, min_size])
    img_array = np.array(img)

    # create two pages twice the size of the origninal image
    page_1 = np.ones([min_size * 2, min_size * 2, 3]) * 255
    page_2 = np.ones([min_size * 2, min_size * 2, 3]) * 255

    for i in range(3):
        tmp = np.tril(img_array[:, :, i], k=0)
        tmp[np.triu_indices(min_size)] = 255
        page_1[min_size:, :min_size, i] = tmp

    for i in range(3):
        tmp_1 = np.triu(img_array[:, :, i], k=1)
        tmp_1[np.tril_indices(min_size, k=0)] = 255
        tmp_1 = np.fliplr(tmp_1)

        tmp_2 = np.tril(tmp_1, k=0)
        tmp_2[np.triu_indices(min_size, k=1)] = 255
        tmp_2 = np.fliplr(tmp_2)

        tmp_3 = np.triu(tmp_1, k=1)
        tmp_3[np.tril_indices(min_size, k=0)] = 255
        tmp_3 = np.fliplr(np.flip(tmp_3))

        page_2[min_size:, :min_size, i] = tmp_2
        page_2[:min_size, min_size:, i] = tmp_3

    page_1 = Image.fromarray(page_1.astype(np.uint8))
    page_2 = Image.fromarray(page_2.astype(np.uint8))

    page_1.save("Page_1.png")
    page_2.save("Page_2.png")

    print(img_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--picture")
    args = parser.parse_args()
    main(args)
