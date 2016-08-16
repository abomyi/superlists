from _sha1 import sha1
import base64
import hmac
import json
import time
import urllib

import boto
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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


@csrf_exempt
def signS3(request):
    AWS_ACCESS_KEY = 'AKIAI5V6LVPJ6TFZXLSA'
    AWS_SECRET_KEY = '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'
    S3_DOMAIN = '.s3.amazonaws.com'
    S3_BUCKET = 'isccyut2'
    S3_PATH = 'https://' + S3_BUCKET + S3_DOMAIN
    
    if request.method=='POST':
        object_name = request.POST.get('s3_object_name')
        mime_type = request.POST.get('s3_object_type')
        expires = int(time.time()+10)
        amz_headers = "x-amz-acl:public-read"
        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY.encode(), put_request.encode(), sha1).digest())
        signature = urllib.parse.quote_plus(signature.strip())
        url = S3_PATH + '/' + object_name
        content = json.dumps({
            'signed_request':'%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
            'url':url,
        })
        return HttpResponse(content)