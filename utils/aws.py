import boto3, uuid, os, mimetypes

class S3ImgUploader:
    """
        AWS_ACCESS_KEY 및 AWS_SECRET_ACCESS_KEY 환경변수 설정 필요
    """
    def __init__(self, file):
        self.file = file

    def upload(self):
        return self.__upload()
    
    def upload_review_img(self):
        return self.__upload('reviews/')
    
    def upload_restaurant_img(self):
        return self.__upload('restaurants/')
        
    def __upload(self, dir:str=""):
        s3_client = boto3.client(
            's3',
            aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        )
        
        url = self.__set_url(dir)
        content_type, _ = mimetypes.guess_type(self.file.name)
        s3_client.upload_fileobj(
            self.file, 
            "yumyum-s3-bucket", 
            url, 
            ExtraArgs={"ContentType": content_type}
        )
        return url

    def __set_url(self, dir:str=""):
        file_name, _ = os.path.splitext(os.path.basename(self.file.name))
        url = 'img'+'/'+dir+uuid.uuid1().hex+'_'+file_name
        return url
    