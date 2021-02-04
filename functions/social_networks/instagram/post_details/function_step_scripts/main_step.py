import json
try:
    import unzip_requirements
except ImportError:
    pass
from pathlib import Path
import logging
from core.constants.base_instagram_constant import LambdaResponseConst
from functions.social_networks.instagram.post_details.request_handlers.post_details_handler import PostDetailsHandler
from functions.social_networks.instagram.post_details.schemas.post_schema import RequestSchema

function_path = str(Path(__file__).resolve().parents[1])


class MainStep:
    logger = logging.getLogger()
    def __init__(self, event, context):
        self.link = event.get('link')
        self.account_info = event['account_info']
        self.context = context
        self.logger = logging.getLogger()

    def crawl_post_details(self):

        response_data = LambdaResponseConst.RESPONSE_FORMAT
        post_info, user_info = PostDetailsHandler(
            post_link=self.link,
            account_cookie=self.account_info.get('info')
        ).crawl_post_details()
        response_data[LambdaResponseConst.DATA_FIELD] = {
            LambdaResponseConst.USER_FIELD: user_info,
            LambdaResponseConst.POST_FIELD: post_info
        }
        return response_data


def lambda_handler(event, context):
    RequestSchema().load(event)
    try:
        return MainStep(event, context).crawl_post_details()
    except Exception as e:
        MainStep.logger.error(e, exc_info=True)
        exception_type = e.__class__.__name__
        exception_message = str(e)
        api_exception_obj = {
            "isError": True,
            "type": exception_type,
            "message": exception_message
        }
        # Create a JSON string
        api_exception_json = json.dumps(api_exception_obj)
        raise LambdaException(api_exception_json)


# Simple exception wrappers
class ClientException(Exception):
    pass

class LambdaException(Exception):
    pass

if __name__ == '__main__':
    # Just for testing. Remove it
    event_test = {
	"link": "https://www.instagram.com/p/CJ5LCqOFU0u/?utm_source=ig_web_copy_link",
	"account_info": {
		"info": {
			"csrftoken": "ped8nryXbMBmLRizll9xUkgD6isUeqlS",
			"ds_user_id": "38279754149",
			"ig_did": "B9FD105A-AA05-4906-AF67-0128EB61B617",
			"mid": "X2gY7QALAAEl58BKpeW7L1jNb7Dw",
			"rur": "FTW",
			"sessionid": "38279754149%3Aka1jEo2By4zWoq%3A26",
			"shbid": "7292",
			"shbts": "1600657655.6954184"
		},
		"account_id": "123124"
	}
}
    response = lambda_handler(event=event_test, context=None)
    print(json.dumps(response))
