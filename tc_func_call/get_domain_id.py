import os
import json
import env_loader
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def get_domain_id(domain: str):
    try:
        cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        common_client = CommonClient("dnspod", "2021-03-23", cred, "", profile=clientProfile)
        params = json.dumps({"Domain": domain})

        return common_client.call_json("DescribeDomain", json.loads(params))
    except TencentCloudSDKException as err:
        return str(err)