import cv2
import numpy as np
from pathlib import Path

# globals
rect_start = None
rect_end = None
rect_center = None
dragging = False
rectangle_size = (1000, 1000)

def get_filepaths(parent_path, extension='mp4', qualifier=None, recursive=True):
    """get all files with a specific extention and qualifier"""
    parent_path = Path(parent_path)
    if qualifier == None:
        pattern = f"*.{extension}"
    else:
        pattern = f"{qualifier}.{extension}"
    filepaths = list(parent_path.rglob(pattern))
    return filepaths


def draw_rectangle(event, x, y, flags, param):
    global rect_center, dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        rect_center = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if dragging:
            rect_center = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False
        rect_center = (x, y)


def read_frame(video_filepath, frame_number=100):

    cap = cv2.VideoCapture(video_filepath)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = cap.read()
    cap.release()

    if not success:
        print(f"Error: Could not read frame {frame_number}.")
        return None

    return frame


def present(img, filepath):

    param_filepath = Path(filepath).with_suffix(".txt", )
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    while True:
        img_copy = img.copy()

        if rect_center:
            top_left = (rect_center[0] - rectangle_size[0] // 2, rect_center[1] - rectangle_size[1] // 2)
            bottom_right = (rect_center[0] + rectangle_size[0] // 2, rect_center[1] + rectangle_size[1] // 2)
            cv2.rectangle(img_copy, top_left, bottom_right, (0, 255, 0), 2)

        cv2.imshow("Image", img_copy)

        key = cv2.waitKey(1) & 0xFF
        if key == 27: 
            break
        elif key == 13:
            if rect_center:
                coordinates = {
                    'center': rect_center,
                    'top_left': top_left,
                    'bottom_right': bottom_right
                }
                print("Rectangle Coordinates:", coordinates)
                with open(param_filepath.as_posix(), 'w') as f:
                    f.write(str(coordinates))
                break
    cv2.destroyAllWindows()

def main():
    parent_path = input('Enter parent directory: ')
    assert Path(parent_path).is_dir(), "the provided parent directory path does not exist"
    filepaths = get_filepaths(parent_path)

    for fp in filepaths:
        if fp.with_suffix(".txt").is_file():
            print('skipping...')
            continue

        else:
            fp = fp.as_posix()
        frame = read_frame(fp, frame_number=100)
        present(frame, fp)
main()


