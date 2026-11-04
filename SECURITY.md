# Security and research-data policy

This is a personal education repository. Default publication visibility is **private**.

- Do not commit API keys, cloud tokens, `.env`, SSH keys or credential files.
- Do not commit private conversation logs, confidential datasets, medical records, unique student records, unreleased model weights or copyrighted source material without explicit rights and authorization.
- Track provenance, restrictions and permitted purposes for every data source and teacher-generation service.
- Use synthetic examples for security testing; sanitize logs, outputs and screenshots.
- Consider data and artifacts from internet repositories untrusted until inspected.
- Do not expose vLLM or other runtime's dynamic adapter-loading administrative endpoints publicly; restrict access to trusted operators and test rollback.
- Check model cards, licenses, dependencies and terms of service before redistribution or commercial use.
- Large model weights, optimizer states and raw datasets should be stored outside Git and referenced by version/hash; never upload secrets as GitHub issue evidence.

If an accidental credential commit occurs, revoke/rotate the secret and remove it from Git history following appropriate procedures; deleting the visible file is not sufficient.
