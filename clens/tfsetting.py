import sys
sys.path.append("D:/PROJECT/C-LENS/darkflow-master")
from darkflow.net.build import TFNet

def init():
    options = {"model":"D:/PROJECT/C-LENS/darkflow-master/cfg/my-tiny-yolo.cfg","backup":"D:/PROJECT/C-LENS/darkflow-master/ckpt", "load":-1, "labels":"D:/PROJECT/C-LENS/darkflow-master/labels.txt", "threshold": 0.4}
    global tfnet
    tfnet = TFNet(options)

def detect_label(img):
    result = tfnet.return_predict(img)
    return result