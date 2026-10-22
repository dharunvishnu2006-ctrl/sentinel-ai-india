from src.logging_setup import setup_logging


def test_setup_logging_twice_adds_no_handlers():
    logger = setup_logging()  # Set up logging once
    before = len(logger.handlers)  # Count handlers after setup
    setup_logging()  # Run setup again, like rerun
    assert len(logger.handlers) == before  # Check count stayed same
