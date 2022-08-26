from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import cv2
import os
import glob
import shutil

def diff(imp1, imp2):
    im1 = cv2.imread(imp1)
    im2 = cv2.imread(imp2)

    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

    s = ssim(im1, im2)

    print(imp1)
    return s

def get_frames(video_path, data_path='data/', captured_path='captured/'):
    cam = cv2.VideoCapture(video_path)

    try:
        if not os.path.exists(data_path):
            os.makedirs(data_path)
    except OSError:
        print('Error: Creating directory of data')

    currentframe = 0
    frame_per_second = cam.get(cv2.CAP_PROP_FPS) 
    frames_captured = 0

    step = 3    #capture image every <step> seconds

    while(True):
        ret, frame = cam.read()

        if ret:    
            if currentframe > (step*frame_per_second):  
                currentframe = 0
                name = os.path.join(data_path, f"{frames_captured:09d}" + '.jpg')
                cv2.imwrite(name, frame)            
                frames_captured+=1
            currentframe += 1           
        if ret==False:
            break

    cam.release()
    cv2.destroyAllWindows()

    filelist = glob.glob(os.path.join(data_path, '*'))
    sorted_list =  sorted(filelist)

    diff_l = []

    for i in range(len(sorted_list)-1):
        diff_l.append(diff(sorted_list[i], sorted_list[i+1]))

    if not os.path.exists(captured_path):
        os.makedirs(captured_path)

    threshold = 0.85

    final_l = []

    for i in range(len(diff_l)):
        if diff_l[i] < threshold:
            final_l.append(shutil.copy(sorted_list[i], captured_path))

    print(final_l)

    return final_l