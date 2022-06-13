import os, sys, django

from django.core.files.storage import get_storage_class

# 현재 파일의 경로를 읽는 코드.
# os.path.abspath(__file__) => 특정 경로의 절대 경로 리턴
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

def upload_files(path):
    default_storage = get_storage_class()()

    
    # os.walk => python 기본 빌트인
    for subdir, dirs, files in os.walk(path):
        # 모든 파일들을 순환
        for file in files:
            full_path = os.path.join(subdir,file)
            # 디렉토리가 아니라 파일일 경우 open 해줍니다. 
            with open(full_path, 'rb') as data:
                default_storage.save(full_path.replace("\\","/")[len(path) + 1:], data)


if __name__ == "__main__":
    upload_files('media')
