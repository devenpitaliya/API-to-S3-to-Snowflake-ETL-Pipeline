
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import FileDataContext
import logging

logger = logging.getLogger(__name__)

def validate_data_with_ge():
    logger.info("Validating data with Great Expectations...")

    context = FileDataContext("/opt/airflow/great_expectations")  # Adjust path to GE project dir

    checkpoint_result: CheckpointResult = context.run_checkpoint(
        checkpoint_name="user_data_checkpoint"
    )

    if not checkpoint_result["success"]:
        logger.error("Data validation failed!")
        raise Exception("❌ Data validation failed. Aborting pipeline.")
    else:
        logger.info("✅ Data validation passed.")
