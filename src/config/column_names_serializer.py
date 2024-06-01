def serialize_column_names(columns):
    return {column: f'f{i}' for i, column in enumerate(columns)}
