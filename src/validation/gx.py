import sys
from great_expectations.checkpoint.types.checkpoint_result import CheckpointResult
from great_expectations.data_context import FileDataContext, DataContext


def gx():
    data_context: FileDataContext = DataContext(
        context_root_dir='gx'
    )

    result: CheckpointResult = data_context.run_checkpoint(
        checkpoint_name='data_checkpoint'
    )

    if not result['success']:
        print('Validation failed!')
        sys.exit(1)

    print('Validation succeeded!')
    sys.exit(0)


if __name__ == "__main__":
    gx()
