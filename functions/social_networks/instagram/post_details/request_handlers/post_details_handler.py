import json
from http import HTTPStatus
import requests
import functions.social_networks.instagram.post_details.constants.post as post_constant
import functions.social_networks.instagram.post_details.constants.user as user_constant


class PostDetailsHandler:
    """
    Class handler to get details of IG post
    """
    def __init__(self, post_link, account_cookie):
        self.link = f"{post_link}?__a=1"
        self.cookie = account_cookie

    def crawl_post_details(self):
        """Get post details base on link + cookie"""

        response_obj = requests.get(self.link, cookies=self.cookie, headers=post_constant.DEFAULT_HEADER)
        if response_obj.status_code == HTTPStatus.NOT_FOUND:
            raise requests.HTTPError("Post not found")
        if response_obj.status_code == HTTPStatus.OK and "/accounts/login/" not in response_obj.url:
            try:
                response_data = response_obj.json()['graphql']['shortcode_media']
            except json.decoder.JSONDecodeError:
                raise requests.HTTPError("Post link is invalid")
            post_info = self.__parse_post_info(response_data)
            user_info = self.__parse_user_info(response_data['owner'])
            post_info[post_constant.ResponseFields.USER_ID] = user_info[user_constant.ResponseFields.USER_ID]
            post_info[post_constant.ResponseFields.USERNAME] = user_info[user_constant.ResponseFields.USERNAME]
            return post_info, user_info
        else:
            raise requests.RequestException("Cookie is expired")

    @staticmethod
    def __parse_post_info(response_data: dict):
        """
        Parse post info if cookie is 'alive'.
        Input:
        - response_data (dict): response data from IG request

        Output:
        - post_info (dict): post info after parsed
        """
        post_info = {
            post_constant.ResponseFields.POST_ID: int(response_data[post_constant.PostConst.POST_ID]),
            post_constant.ResponseFields.POST_IMG: response_data[post_constant.PostConst.POST_IMG],
            post_constant.ResponseFields.POST_TYPE: response_data[post_constant.PostConst.POST_TYPE],
            post_constant.ResponseFields.CONTENT: [
                content['node']['text'] for content in response_data[post_constant.PostConst.CONTENT]['edges']
            ],
            post_constant.ResponseFields.CREATED_TIME: response_data[post_constant.PostConst.CREATED_TIME],
            post_constant.ResponseFields.SHORTCODE: response_data[post_constant.PostConst.SHORTCODE],
            post_constant.ResponseFields.NUM_LIKE: response_data[post_constant.PostConst.NUM_LIKE]['count'],
            post_constant.ResponseFields.NUM_COMMENT: response_data[post_constant.PostConst.NUM_COMMENT]['count'],
        }

        if response_data[post_constant.PostConst.IS_VIDEO]:
            post_info[post_constant.ResponseFields.NUM_VIEW] = response_data[post_constant.PostConst.NUM_VIEW]

        if response_data[post_constant.PostConst.LOCATION]:
            post_info[post_constant.ResponseFields.LOCATION] = response_data[post_constant.PostConst.LOCATION]
        return post_info

    @staticmethod
    def __parse_user_info(response_data: dict):
        """
        Parse owner info if cookie is 'alive'.
        Input:
        - response_data (dict): response data from IG request

        Output:
        - user_info (dict): user info after parsed
        """
        user_info = {
            user_constant.ResponseFields.AVATAR: response_data[user_constant.UserConst.AVATAR],
            user_constant.ResponseFields.USER_ID: int(response_data[user_constant.UserConst.USER_ID]),
            user_constant.ResponseFields.USERNAME: response_data[user_constant.UserConst.USERNAME],
            user_constant.ResponseFields.FULL_NAME: response_data[user_constant.UserConst.FULL_NAME],
            user_constant.ResponseFields.IS_VERIFY: response_data[user_constant.UserConst.IS_VERIFY],
            user_constant.ResponseFields.NUM_PHOTO: response_data[user_constant.UserConst.NUM_PHOTO]['count'],
            user_constant.ResponseFields.NUM_FOLLOWER: response_data[user_constant.UserConst.NUM_FOLLOWER]['count'],
        }
        return user_info

if __name__ == '__main__':
    link = "https://www.instagram.com/p/CKU_Mn9BrXY"
    cookie = {
    "csrftoken": "ped8nryXbMBmLRizll9xUkgD6isUeqlS",
    "ds_user_id": "38279754149",
    "ig_did": "B9FD105A-AA05-4906-AF67-0128EB61B617",
    "mid": "X2gY7QALAAEl58BKpeW7L1jNb7Dw",
    "rur": "FTW",
    "sessionid": "38279754149%3Aka1jEo2By4zWoq%3A26",
    "shbid": "7292",
    "shbts": "1600657655.6954184",
}
    a, b = PostDetailsHandler(link, cookie).crawl_post_details()
    print(a, b)