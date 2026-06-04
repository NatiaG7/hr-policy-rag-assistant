# HR policy documents

Do **not** commit proprietary HR PDFs (company-specific policies you do not have rights to share).

## Included sample (safe to publish)

- `sample/employee_handbook_sample.txt` — **synthetic demo** handbook used by `scripts/build_index.py` by default

## Add your own documents

Place files in `data/raw/`:

```
data/raw/your_policy.pdf
data/raw/another_section.txt
```

Then rebuild the index:

```bash
python scripts/build_index.py --document data/raw/your_policy.pdf
```

## AWS S3 or URL download (optional)

Use [scripts/download_data.py](../scripts/download_data.py) after configuring [`.env.example`](../.env.example):

```bash
cp .env.example .env
# Edit AWS_S3_BUCKET, AWS_S3_KEY, or POLICY_DOCUMENT_URL

pip install boto3   # only if using S3
python scripts/download_data.py --s3-bucket YOUR_BUCKET --s3-key hr/policy.pdf
python scripts/build_index.py --document data/raw/policy.pdf
```

## Supported formats

- `.pdf` — via LangChain `PyPDFLoader`
- `.txt`, `.md` — plain text via `TextLoader`
