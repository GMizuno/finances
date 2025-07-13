# Yahoo Finance in GCP
    

Shell command to test the deployment 
```shell
curl -X POST https://finance-XXXXXXX.us-east1.run.app \
-H "Authorization: bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json" \
-d '{
  "end": "2025-02-28",
  "start": "2024-01-01",
  "tickets": [
    "B5P211.SA",
    "SPXB11.SA",
    "IRFM11.SA",
    "DEBB11.SA",
    "IB5M11.SA",
    "BRL=X"
  ]
}'
```
