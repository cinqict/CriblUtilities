#Latest Python 3.13 image (slim version for smaller size)
FROM python:3.13.2-slim

RUN pip install --upgrade pip pipx && \
    pip cache purge && \
    pipx install --force cribl-utilities


ENV PATH="/root/.local/bin:$PATH"

ENTRYPOINT ["cribl-utilities"]
#test