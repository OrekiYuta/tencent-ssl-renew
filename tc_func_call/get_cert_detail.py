import os
import json
import env_loader
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def get_certificate_detail(certificate_id: str):
    try:
        cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

        http_profile = HttpProfile()
        http_profile.endpoint = "ssl.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        common_client = CommonClient("ssl", "2019-12-05", cred, "", profile=client_profile)
        params = json.dumps({"CertificateId": certificate_id})

        return common_client.call_json("DescribeCertificateDetail", json.loads(params))
    except TencentCloudSDKException as err:
        return str(err)


if __name__ == '__main__':
    certificate_id = "MwYz6NPX"
    result = get_certificate_detail(certificate_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))