import json
from tc_func_call.list_certs_info import get_certificates


def main():
    certificates = get_certificates()
    print(json.dumps(certificates, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

'''
1.list_certs_info
2.get_cert_detail
3.create_dns_record
4.trigger_cert_complete
'''