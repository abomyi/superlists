import boto
from django.shortcuts import render

from superlists.settings import GS_ACCESS_KEY, GS_SECRET_KEY, GS_BUCKET_NAME


# Create your views here.
def upload(request):
    context = {}
    if request.method=='POST':
        fileURL = request.POST.get('fileURL')
        context.update({'fileURL':fileURL})
#          if 'file' in request.FILES:
#              url = fileUpload(request)
#              context.update({'url':url})
    return render(request, 'upload/upload.html', context)


def fileUpload(request):
    
    conn = boto.connect_gs(gs_access_key_id=GS_ACCESS_KEY,
                            gs_secret_access_key=GS_SECRET_KEY)
    bucket = conn.get_bucket(GS_BUCKET_NAME)
    fileToUpload = request.FILES['file']
    cloudFileName = 'test/recordAppy/'+fileToUpload.name
    fpic = boto.gs.key.Key(bucket)
    fpic.key = cloudFileName
    fpic.set_contents_from_file(fileToUpload)
        
    url = fpic.generate_url(expires_in=86400)
    
    return url  #在catch時要依靠json來傳值, 但json不支援bytes型態, 故在此轉為str
