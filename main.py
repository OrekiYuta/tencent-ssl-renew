import json
import env_loader
from tc_func_call.get_domain_id import get_domain_id
from tc_func_call.list_certs_info import get_certificates
from tc_func_call.create_dns_record import create_record_batch
from tc_func_call.get_cert_detail import get_certificate_detail
from tc_func_call.trigger_cert_complete import complete_certificate


def main():
    """
    Main function to automate SSL certificate verification:
    1. Retrieve pending certificates
    2. Fetch authentication details
    3. Obtain domain ID
    4. Create DNS records for verification
    5. Trigger certificate completion
    """

    # Retrieve all pending certificates
    certs_params = {}
    certificates_response = get_certificates(certs_params)

    if not certificates_response or "Response" not in certificates_response:
        print("❌ Error: Unable to fetch certificate information.")
        return

    certificates = certificates_response["Response"].get("Certificates", [])

    for cert in certificates:
        if cert.get("Status") == 0:  # Certificate under review
            certificate_id = cert.get("CertificateId")
            domain = cert.get("Domain")
            print(f"🔍 Processing Certificate ID: {certificate_id} | Domain: {domain}")

            # Get certificate details
            cert_detail_response = get_certificate_detail(certificate_id)
            if not cert_detail_response or "Response" not in cert_detail_response:
                print(f"❌ Error: Failed to retrieve details for Certificate ID: {certificate_id}")
                continue

            dv_auths = cert_detail_response["Response"].get("DvAuthDetail", {}).get("DvAuths", [])
            if not dv_auths:
                print(f"⚠️ Warning: No authentication details found for Certificate ID: {certificate_id}")
                continue

            dv_auth = dv_auths[0]
            auth_value = dv_auth.get("DvAuthValue")
            auth_domain = dv_auth.get("DvAuthDomain")
            auth_subdomain = dv_auth.get("DvAuthSubDomain")
            auth_verify_type = dv_auth.get("DvAuthVerifyType")

            if not auth_value or not auth_subdomain:
                print(f"⚠️ Warning: Incomplete authentication info for Certificate ID: {certificate_id}")
                continue

            # Retrieve domain ID
            domain_id_response = get_domain_id(auth_domain)
            if not domain_id_response or "Response" not in domain_id_response:
                print(f"❌ Error: Unable to retrieve domain ID for: {auth_domain}")
                continue

            domain_id = domain_id_response["Response"].get("DomainInfo", {}).get("DomainId")
            if not domain_id:
                print(f"❌ Error: Domain ID not found for: {auth_domain}")
                continue

            # Create DNS record for domain verification
            params = {
                "DomainIdList": [str(domain_id)],
                "RecordList": [
                    {
                        "RecordType": auth_verify_type,
                        "Value": auth_value,
                        "SubDomain": auth_subdomain,
                    }
                ],
            }

            create_record_response = create_record_batch(params)
            if create_record_response.get("Response", {}).get("Error"):
                print(f"❌ Error: Failed to create DNS record for {auth_subdomain} | Reason: {create_record_response['Response']['Error']}")
            else:
                print("✅ DNS record successfully created:")
                print(f"   📌 Domain ID    : {domain_id}")
                print(f"   📌 Record Type  : {auth_verify_type}")
                print(f"   📌 Value        : {auth_value}")
                print(f"   📌 SubDomain    : {auth_subdomain}")

            # Trigger certificate completion
            complete_certificate(certificate_id)
            print(f"🎉 Certificate completion triggered for Certificate ID: {certificate_id}\n")


if __name__ == "__main__":
    main()
