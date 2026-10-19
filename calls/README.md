# calls/

Put exported call-log JSON files here (one per call), for example:

```bash
curl -X GET "https://api.retellai.com/get-call/<CALL_ID>" \
  -H "Authorization: Bearer $RETELL_API_KEY" > calls/<CALL_ID>.json
python scripts/audit_ftl.py calls/*.json
```

Never commit your API key.
