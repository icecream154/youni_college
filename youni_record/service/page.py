from django.http import HttpResponse

from project_config import PROJECT_ROOT


def get_page(request):
    html = None
    try:
        with open(PROJECT_ROOT + '/youni_record/html/page.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(e)

    if not html:
        html = u'对不起加载出错了'
    return HttpResponse(html)