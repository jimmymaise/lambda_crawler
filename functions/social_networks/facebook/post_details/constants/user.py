"""
Class for get User info from post
"""


class UserLoginRegexStr:
    "Regex var for User info with login"
    USER_ID = r'props\":\{\"actorID\":(\d+)\,\"isViewerAdmin\"'
    USERNAME = r'rel\=\"canonical\" href\=\"https\:\/\/www\.facebook\.com\/(\S+)/(?:posts|videos)/'
    USER_AVATAR = r'story\_bucket\".*\,\"profile\_picture\"\:\{\"uri\"\:\"(\S+)\"\,'
    FULL_NAME = r'TEST'


class UserNLoginRegexStr:
    "Regex var for User info without login"
    USER_ID = r'props\:\{profileID\:\"(\d+)\"\}'
    USERNAME = r'rel\=\"canonical\" href\=\"https\:\/\/www\.facebook\.com\/(\S+)/(?:posts|videos)/'
    USER_AVATAR = r'img class\="scaledImageFitWidth img" src\="(\S+)\" data\-src\='
    FULL_NAME = r'meta property\=\"og\:title\" content\=\"(.*)" \/\>\<meta property\=\"og\:description\"'
    