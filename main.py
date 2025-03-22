import json
import env_loader
from tc_func_call.list_certs_info import get_certificates
from tc_func_call.get_cert_detail import get_certificate_detail
from tc_func_call.create_dns_record import create_record_batch
from tc_func_call.trigger_cert_complete import complete_certificate


def main():
    # List all certificates
    certs_params = {}
    certificates = get_certificates(certs_params)
    print("Certificates List:")
    print(json.dumps(certificates, indent=2, ensure_ascii=False))

    # Get details of a specific certificate
    if certificates and "Certificates" in certificates and certificates["Certificates"]:
        cert_id = certificates["Certificates"][0]["CertificateId"]
        cert_detail = get_certificate_detail({"CertificateId": cert_id})
        print("\nCertificate Detail:")
        print(json.dumps(cert_detail, indent=2, ensure_ascii=False))

        # Create a DNS record for verification
        dns_params = {
            "DomainIdList": ["example.com"],
            "RecordList": [{"RecordType": "TXT", "Value": "verification-code", "SubDomain": "_acme-challenge"}]
        }
        dns_result = create_record_batch(dns_params)
        print("\nDNS Record Creation Result:")
        print(json.dumps(dns_result, indent=2, ensure_ascii=False))

        # Trigger certificate completion process
        completion_result = complete_certificate({"CertificateId": cert_id})
        print("\nCertificate Completion Result:")
        print(json.dumps(completion_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
