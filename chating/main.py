from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# 用于存储消息的列表
messages = []

def index(request):
    """渲染主页"""
    return render(request, 'chat/index.html')

@csrf_exempt
def send_message(request):
    """处理发送消息的请求"""
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        message = data.get('message')
        
        if username and message:
            messages.append({
                'username': username,
                'message': message
            })
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_messages(request):
    """获取所有消息"""
    return JsonResponse({'messages': messages}) 