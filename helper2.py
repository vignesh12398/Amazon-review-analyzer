def find_column(df, possible_columns):
    """
    Find the first matching column from the dataframe.
    Returns the actual column name or None.
    """

    normalized_cols = {
        col.lower().strip().replace(" ", "_"): col
        for col in df.columns
    }

    for col in possible_columns:
        key = col.lower().strip().replace(" ", "_")
        if key in normalized_cols:
            return normalized_cols[key]

    return None