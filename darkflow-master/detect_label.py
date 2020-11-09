from darkflow.net.build import TFNet

def detect_label(img):
    options = {"model":"C:/darkflow-master/cfg/my-tiny-yolo.cfg","backup":"C:/darkflow-master/ckpt", "load":-1, "labels":"C:/darkflow-master/labels.txt"}
    tfnet = TFNet(options)
    result = tfnet.return_predict(img)
    return result