import os
import json
import env_loader
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def get_certificates(params: dict):
    try:
        cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

        httpProfile = HttpProfile()
        httpProfile.endpoint = "ssl.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        common_client = CommonClient("ssl", "2019-12-05", cred, "", profile=clientProfile)
        response = common_client.call_json("DescribeCertificates", params)
        return response
    except TencentCloudSDKException as err:
        return {"error": str(err)}
