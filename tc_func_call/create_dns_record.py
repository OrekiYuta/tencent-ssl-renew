import os
import env_loader
from tencentcloud.common.common_client import CommonClient
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile


def create_record_batch(params: dict):
    try:
        cred = credential.Credential(os.getenv("SECRET_ID"), os.getenv("SECRET_KEY"))

        http_profile = HttpProfile()
        http_profile.endpoint = "dnspod.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile

        common_client = CommonClient("dnspod", "2021-03-23", cred, "", profile=client_profile)

        return common_client.call_json("CreateRecordBatch", params)
    except TencentCloudSDKException as err:
        return str(err)


if __name__ == "__main__":
    params = {
        "DomainIdList": ["abc.gd.cn"],
        "RecordList": [{"RecordType": "TXT", "Value": "abc", "SubDomain": "A"}]
    }
    result = create_record_batch(params)
    print(result)
