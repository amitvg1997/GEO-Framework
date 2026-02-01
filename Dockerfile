FROM public.ecr.aws/lambda/python:3.13

# -----------------------------
# Install Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Download NLTK data (read-only safe)
# -----------------------------
RUN mkdir -p /var/task/nltk_data && \
    python - <<EOF
import nltk
nltk.data.path.insert(0, "/var/task/nltk_data")
nltk.download("cmudict", download_dir="/var/task/nltk_data", quiet=True)
EOF

# -----------------------------
# Download SpaCy model (USE md, not lg)
# -----------------------------
RUN python -m spacy download en_core_web_md

# -----------------------------
# Pre-download SentenceTransformer model
# (CRITICAL FIX)
# -----------------------------
RUN python - <<EOF
from sentence_transformers import SentenceTransformer
SentenceTransformer("all-MiniLM-L6-v2")
EOF

# -----------------------------
# Copy application code
# -----------------------------
COPY app.py ./app.py
COPY metrics ./metrics

# -----------------------------
# Lambda entry point
# -----------------------------
CMD ["app.lambda_handler"]