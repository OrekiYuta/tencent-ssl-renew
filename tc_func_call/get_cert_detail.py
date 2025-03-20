import json
import os

from dotenv import load_dotenv
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

load_dotenv()

try:
    cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

    httpProfile = HttpProfile()
    httpProfile.endpoint = "ssl.tencentcloudapi.com"
    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile

    params = "{\"CertificateId\":\"MpXfb2EY\"}"
    common_client = CommonClient("ssl", "2019-12-05", cred, "", profile=clientProfile)
    print(common_client.call_json("DescribeCertificateDetail", json.loads(params)))
except TencentCloudSDKException as err:
    print(err)
