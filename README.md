curl -X POST https://finance-1077543354314.us-east1.run.app \
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
    "IB5M11.SA".
    "BRL=X"
  ]
}'


SELECT `Date`, Close, lag_close, 100*(Close - lag_close)/Close
FROM (
SELECT *, LAG(Close)
    OVER (PARTITION BY Ticket ORDER BY `Date` ASC) AS lag_close FROM finances.finance_raw 
WHERE Ticket = 'SPXB11.SA'
ORDER BY `Date` DESC
)
