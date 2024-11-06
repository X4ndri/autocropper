from pathlib import Path
import ast
import cv2


def get_filepaths(parent_path, extension='mp4', qualifier=None, recursive=True):
    """get all files with a specific extention and qualifier"""
    parent_path = Path(parent_path)
    if qualifier == None:
        pattern = f"*.{extension}"
    else:
        pattern = f"{qualifier}.{extension}"
    filepaths = list(parent_path.rglob(pattern))
    return filepaths


def crop(filepath):
    
    params_filepath = filepath.with_suffix('.txt')
    with open(params_filepath.as_posix()) as file:
        params_ = file.read()
    params = ast.literal_eval(params_)

    top_left = params['top_left']
    bottom_right = params['bottom_right']
    x_start, y_start = top_left
    x_end, y_end = bottom_right

    cap = cv2.VideoCapture(filepath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = x_end - x_start
    height = y_end - y_start

    output_path = filepath.with_name(filepath.stem + "_cropped.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cropped_frame = frame[y_start:y_end, x_start:x_end]
        out.write(cropped_frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()



def main():
#     parent_path = input("Enter parent directory path: ")
#     assert Path(parent_path).is_dir(), "The provided parent path does not exist"
    filepaths = get_filepaths(r"C:\Users\aaqad\repos\autocropper")
    print(filepaths)
    for fp in filepaths:
        try:
            assert fp.with_suffix('.txt').is_file(), "No params file found for recording: {fp}"
            crop(fp)
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()