# =====================================================
# AWS Lambda Python Local Development Dockerfile
# =====================================================
# This Dockerfile creates an environment that mimics
# AWS Lambda's Python 3.13 runtime for local testing.
# =====================================================

FROM public.ecr.aws/lambda/python:3.13

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ${LAMBDA_TASK_ROOT}/

# Set the default handler (can be overridden at runtime)
# Example: GetItems handler
CMD [ "features.items.presentation.get_handler.handler" ]
