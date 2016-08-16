function uploadToS3(s3URL, elemID, signS3Request, callback){
  var s3upload = new S3Upload({
    s3_object_name: s3URL,
    file_dom_selector: elemID,
    s3_sign_put_url: signS3Request,
  }, callback);
  return true;
}


(function() {

    window.S3Upload = (function() {

      S3Upload.prototype.s3_object_name = 'default_name';

      S3Upload.prototype.s3_sign_put_url = '/signS3put';

      S3Upload.prototype.file_dom_selector = 'file_upload';

      S3Upload.prototype.onFinishS3Put = function(public_url, callback) {
        callback();
        return console.log('base.onFinishS3Put()', public_url);
      };

      S3Upload.prototype.onProgress = function(percent, status) {
        return console.log('base.onProgress()', percent, status);
      };

      S3Upload.prototype.onError = function(status) {
        return console.log('base.onError()', status);
      };

      function S3Upload(options, callback) {
        if (options == null) options = {};
        for (option in options) {
          this[option] = options[option];
        }
        this.handleFileSelect(document.getElementById(this.file_dom_selector), callback);
      }

      S3Upload.prototype.handleFileSelect = function(file_element, callback) {
        var f, files, output, _i, _len, _results;
        this.onProgress(0, 'Upload started.');
        files = file_element.files;
        output = [];
        _results = [];
        for (_i = 0, _len = files.length; _i < _len; _i++) {
          f = files[_i];
          _results.push(this.uploadFile(f, callback));
        }
        return _results;
      };

      S3Upload.prototype.createCORSRequest = function(method, url) {
        var xhr;
        xhr = new XMLHttpRequest();
        if (xhr.withCredentials != null) {
          xhr.open(method, url, true);
        } else if (typeof XDomainRequest !== "undefined") {
          xhr = new XDomainRequest();
          xhr.open(method, url);
        } else {
          xhr = null;
        }
        return xhr;
      };

      S3Upload.prototype.executeOnSignedUrl = function(file, callback, callback2) {
        var this_s3upload, xhr;
        this_s3upload = this;
        var params = 's3_object_type=' + file.type + '&s3_object_name=' + this.s3_object_name;
        xhr = new XMLHttpRequest();
        xhr.open('POST', this.s3_sign_put_url, true);
        xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xhr.overrideMimeType('text/plain; charset=x-user-defined');
        xhr.onreadystatechange = function(e) {
          var result;
          if (this.readyState === 4 && this.status === 200) {
            try {
              result = JSON.parse(this.responseText);
            } catch (error) {
              this_s3upload.onError('Signing server returned some ugly/empty JSON: "' + this.responseText + '"');
              return false;
            }
            return callback(result.signed_request, result.url, callback2);
          } else if (this.readyState === 4 && this.status !== 200) {
            return this_s3upload.onError('Could not contact request signing server. Status = ' + this.status);
          }
        };
        return xhr.send(params);
      };

      S3Upload.prototype.uploadToS3 = function(file, url, public_url, callback) {
        var this_s3upload, xhr;
        this_s3upload = this;
        xhr = this.createCORSRequest('PUT', url);
        if (!xhr) {
          this.onError('CORS not supported');
        } else {
          xhr.onload = function() {
            if (xhr.status === 200) {
              this_s3upload.onProgress(100, 'Upload completed.');
              return this_s3upload.onFinishS3Put(public_url, callback);
            } else {
              return this_s3upload.onError('Upload error: ' + xhr.status);
            }
          };
          xhr.onerror = function() {
            return this_s3upload.onError('XHR error.');
          };
          xhr.upload.onprogress = function(e) {
            var percentLoaded;
            if (e.lengthComputable) {
              percentLoaded = Math.round((e.loaded / e.total) * 100);
              return this_s3upload.onProgress(percentLoaded, percentLoaded === 100 ? 'Finalizing.' : 'Uploading.');
            }
          };
        }
        xhr.setRequestHeader('Content-Type', file.type);
        xhr.setRequestHeader('x-amz-acl', 'public-read');
        return xhr.send(file);
      };

      S3Upload.prototype.uploadFile = function(file, callback) {
        var this_s3upload;
        this_s3upload = this;
        return this.executeOnSignedUrl(file, function(signedURL, publicURL, callback2) {
          return this_s3upload.uploadToS3(file, signedURL, publicURL, callback2);
        }, callback);
      };

      return S3Upload;

    })();

  }).call(this);