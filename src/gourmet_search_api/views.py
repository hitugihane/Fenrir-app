import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings

HOTPEPPER_API_URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
# APIキーの使用
API_KEY = settings.HOTPEPPER_API_KEY

def index(request):
    # index.htmlを表示するためのビュー
    return render(request, 'index.html')

def fetch_shops(request):
    latitude = float(request.GET.get('lat'))
    longitude = float(request.GET.get('lng'))
    page_number = request.GET.get('page', 1)

    shops = fetch_and_combine_shops(latitude, longitude)
    
    # ページネーション
    paginator = Paginator(shops, 5)  # 5店舗ごとにページネーション
    page_obj = paginator.get_page(page_number)
    
    # JSONで返すデータを準備
    data = {
        'shops': list(page_obj.object_list),
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': paginator.num_pages,
        'current_page': page_obj.number
    }

    return JsonResponse(data)

def calculate_surrounding_points(latitude, longitude, distance=0.02):# 0.02はおおよ3kmでした（Googlemapでずらじてみて試しました）
    # 緯度経度を少し変化させることで4つの周辺地点を生成
    points = [
        (latitude + distance, longitude),
        (latitude - distance, longitude),
        (latitude, longitude + distance),
        (latitude, longitude - distance),
    ]
    return points

def fetch_and_combine_shops(lat, lng):
    points = calculate_surrounding_points(lat, lng)
    responses = []
    for point in points:
        params = {
            'key': API_KEY,
            'lat': point[0],
            'lng': point[1],
            'range': 5,  # 検索範囲をここで調整可能
            'format': 'json',
        }
        response = requests.get(HOTPEPPER_API_URL, params=params)
        if response.status_code == 200:
            responses.append(response.json()['results']['shop'])
    
    # 結果を統合し、重複を除外
    all_shops = list({shop['id']: shop for shops in responses for shop in shops}.values())
    return all_shops




