import os

from aws_lambda_powertools import Logger, Metrics

env = os.getenv("ENVIROMENTS", "local")

if env.lower() == "local":
    os.environ["POWERTOOLS_DEV"] = "1"
    logger = Logger(service="DataExtractionLocal")
    metrics = Metrics(namespace="Finance", service="DataExtractionLocal")
else:
    logger = Logger(service="DataExtraction")
    metrics = Metrics(namespace="Finance", service="DataExtraction")
