import os
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse  # 返回json格式的数据
from django.conf import settings  # 配置文件


@csrf_exempt
def upload_file(request):
    # 获取表单上传的图片
    file = request.FILES.get('upload')
    # 返回uid
    uid = str(uuid.uuid4()).replace('-', '')
    records = str(file.name).split('.')
    records[0] = uid
    file.name = '.'.join(records)
    file_path = os.path.join(settings.MEDIA_ROOT, 'upload/', file.name)
    print(file_path)

    # 上传图片
    with open(file_path, 'wb+') as f:
        for chunk in file.chunks():
            f.write(chunk)

    url = 'media/upload/' + file.name
    ret_data = {
        'url': url,
        'uploaded': '1',
        'filename': file.name
    }
    return JsonResponse(ret_data)
