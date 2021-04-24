import cv2
import time
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from utils import convert_image, chars_to_img, get_img_in_ascii, get_tile_img_dim


if __name__ == "__main__":
    c = input("Choose what would you like to do:\nl - Load image to transform\nt - Translate you webcam\n")
    if c == 'l':
        root = Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        filename = askopenfilename(filetypes=[("Image files", "*.png, *.jpg"), ("All Files", "*.*")])
        img = convert_image(img_path=filename)
        img_in_ascii = get_img_in_ascii(img, get_tile_img_dim(img.shape))

        f = open("output.txt", 'w')
        for row in img_in_ascii:
            f.write(row + '\n')

        chars_to_img(img_in_ascii).save('sample-out.jpg')
    elif c == 't':
        # you should change frame rate based on how much time it takes to process img on your pc
        frame_rate = 7
        prev = 0
        cap = cv2.VideoCapture()
        cap.open(0)

        _, frame = cap.read()

        tile_img_dim = get_tile_img_dim(frame.shape)

        while True:
            _, frame = cap.read()

            time_elapsed = time.time() - prev
            res, image = cap.read()

            if time_elapsed > 1. / frame_rate:
                prev = time.time()

                img_in_ascii = get_img_in_ascii(frame, tile_img_dim)
                cv2.imshow("camCapture", np.array(chars_to_img(img_in_ascii)))
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
    else:
        print("Sorry. No such command.")
