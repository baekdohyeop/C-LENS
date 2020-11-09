import urllib.request
import ssl
from bs4 import BeautifulSoup as BS
from django.views.decorators.csrf import csrf_exempt
import json
import traceback
import os
import io
import numpy as np
import cv2
from threading import Thread
from multiprocessing import Process, Queue
from django.http import JsonResponse
from django.http import HttpResponse
from tfsetting import detect_label
import time
import sys
sys.path.append('D:/PROJECT/C-LENS/clens')


def detect_text(img, coordinate, q):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    dst = img[coordinate[1]:coordinate[3], coordinate[0]:coordinate[2]]
    content = cv2.imencode('.jpg', dst)[1].tostring()

    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        if texts[0].description:
            tags = texts[0].description.split('\n')
            if len(tags) == 5:
                for i in range(5):
                    if ('원' in tags[i] or '윈' in tags[i] or '뭔' in tags[i] or tags[i].replace(',', '').isdecimal()) and ('/' not in tags[i]) and ('/' in tags[i - 1]):
                        base_url = 'https://www.google.co.kr/search'
                        target = tags[0] + ' ' + tags[1]
                        values = {
                            'q': target,
                            'oq': target,
                            'aqs': 'chrome..69i57.35694j0j7',
                            'sourceid': 'chrome',
                            'ie': 'UTF-8',
                        }
                        hdr = {'User-Agent': 'Mozilla/5.0'}
                        query_string = urllib.parse.urlencode(values)
                        req = urllib.request.Request(
                            base_url + '?' + query_string, headers=hdr)
                        context = ssl._create_unverified_context()

                        try:
                            res = urllib.request.urlopen(req, context=context)
                        except:
                            traceback.print_exc()

                        html_data = BS(res.read(), 'lxml')
                        calibrate = html_data.find('a', {'id': 'scl'})

                        if calibrate:
                            target = calibrate.text
                        else:
                            calibrate = html_data.find(
                                'div', {'class': 'MUxGbd v0nnCb lyLwlc'})

                            if calibrate:
                                target = calibrate.find('a').text

                        base_url = "https://search.naver.com/search.naver"
                        values = {
                            'query': target,
                            'ie': 'UTF-8',
                        }
                        query_string = urllib.parse.urlencode(values)
                        req = urllib.request.Request(base_url + '?' + query_string)

                        try:
                            res = urllib.request.urlopen(req)
                        except:
                            traceback.print_exc()

                        html_data = BS(res.read(), 'lxml').find('div', {'class':'sp_keyword'})

                        if html_data and html_data.find('em'):
                            target = html_data.find('em').text

                        client_id = "5chemkLs42Gj4WSJH5Q6"
                        client_secret = "mTYeI7E0vX"
                        encText = urllib.parse.quote(
                            "{}".format(target))
                        url = "https://openapi.naver.com/v1/search/shop.json?query=" + encText
                        request = urllib.request.Request(url)
                        request.add_header("X-Naver-Client-Id", client_id)
                        request.add_header(
                            "X-Naver-Client-Secret", client_secret)
                        response = urllib.request.urlopen(request)
                        rescode = response.getcode()

                        if(rescode == 200):
                            data = response.read().decode('utf-8')
                            products = json.loads(data)

                            if int(products["display"]) == 0:
                                result = {}
                                result['search_word'] = target
                                result['product_name'] = None
                                result['coordinate'] = coordinate
                                result['link'] = None
                                result['low_price'] = None
                                result['score'] = None
                                result['thumbnail'] = None
                                q.put(result)
                            else:
                                idx = -1
                                for j in range(int(products["display"])):
                                    if int(products["items"][j]["productType"]) == 1:
                                        idx = j

                                if idx != -1:
                                    result = {}
                                    result['search_word'] = target
                                    result['product_name'] = products["items"][idx]["title"].replace('<b>', '').replace('</b>', '')
                                    result['coordinate'] = coordinate
                                    result['link'] = products["items"][idx]["link"]
                                    result['low_price'] = products["items"][idx]["lprice"]
                                    result['score'] = None
                                    if 'image' in products["items"][idx]:
                                        result['thumbnail'] = products["items"][idx]["image"]
                                    else:
                                        result['thumbnail'] = None
                                    q.put(result)
                                else:
                                    result = {}
                                    result['search_word'] = target
                                    result['product_name'] = products["items"][0]["title"].replace('<b>', '').replace('</b>', '')
                                    result['coordinate'] = coordinate
                                    result['link'] = products["items"][0]["link"]
                                    result['low_price'] = products["items"][0]["lprice"]
                                    result['score'] = None
                                    if 'image' in products["items"][idx]:
                                        result['thumbnail'] = products["items"][0]["image"]
                                    else:
                                        result['thumbnail'] = None
                                    q.put(result)
                        else:
                            print("HTTP Error with NAVER")
            else:
                return
    else:
        return


def part_process(image, coordinates, q):
    threads = []

    for coordinate in coordinates:
        thread = Thread(target=detect_text, args=(image, coordinate, q))
        threads.append(thread)
        thread.start()

        if len(threads) >= 8:
            for thread in threads:
                thread.join()
            threads.clear()

    if len(threads):
        for thread in threads:
            thread.join()

    return


def index(request):
    if request.method == "POST":
        if request.FILES.__len__() != 0:
            count = 0
            image = cv2.imdecode(np.frombuffer(
                request.FILES['file'].read(), np.uint8), -1)
            labels = detect_label(image)
            coordinates = []

            for label in labels:
                count += 1
                row_start = label['topleft']['y']
                row_end = label['bottomright']['y']
                col_start = label['topleft']['x']
                col_end = label['bottomright']['x']
                coordinates.append((col_start, row_start, col_end, row_end))

            q = Queue()
            count = count // 2

            process1 = Process(target=part_process, args=(
                image, coordinates[:count], q))
            process2 = Process(target=part_process, args=(
                image, coordinates[count:], q))

            process1.start()
            process2.start()

            process1.join()
            process2.join()

            products = []

            while not q.empty():
                info = q.get()
                products.append(info)
            q.close()

            result = {}
            result['products'] = products

            return JsonResponse(
                result,
                json_dumps_params={'ensure_ascii': False},
            )
        else:
            return HttpResponse(False)
