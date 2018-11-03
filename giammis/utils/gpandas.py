import pandas as pd
from collections import Counter
from functools import reduce
from sklearn.utils import shuffle

from giammis.utils.generic import identity_func


def optimize_memory_usage(df, types_to_numeric=None, types_to_category=None, verbose=False):
    """

    Args:
        df (DataFrame):
        types_to_numeric (list|None):
        types_to_category (list|None):
        verbose (bool):

    Returns:
        DataFrame:
    """
    df_to_optimize = pd.DataFrame(df.copy())
    if types_to_numeric is None:
        types_to_numeric = ['float', 'integer']
    if types_to_category is None:
        types_to_category = ['object']
    # To numeric
    for type_to_numeric in types_to_numeric:
        type_to_numeric_columns = df_to_optimize.select_dtypes(include=[type_to_numeric]).columns
        for col in type_to_numeric_columns:
            df_to_optimize[col] = pd.to_numeric(df_to_optimize[col], downcast=type_to_numeric)
    # To category
    for type_to_category in types_to_category:
        type_to_category_columns = df_to_optimize.select_dtypes(include=[type_to_category]).columns
        for col in type_to_category_columns:
            if len(df_to_optimize[col].unique()) < len(df_to_optimize[col]) // 4:
                df_to_optimize[col] = df_to_optimize[col].astype('category')
    if verbose:
        memory_before_mb = df.memory_usage(deep=True).sum() / (2.0 ** 20)
        memory_after_mb = df_to_optimize.memory_usage(deep=True).sum() / (2.0 ** 20)
        print("Memory usage before:\t\t\t{} MB".format(memory_before_mb))
        print("Memory usage after:\t\t\t{} MB".format(memory_after_mb))
        print("Percentage of the optimized file:\t{} %".format(memory_after_mb / memory_before_mb * 100.0))
    return df_to_optimize


# TODO unittest and maybe pass only a list without first value
def join_multiple(df_initial, df_list, on, how='inner'):
    """

    Args:
        df_initial (DataFrame):
        df_list (list[DataFrame]):
        on (str|list[str]):
        how (str):

    Returns:
        DataFrame:
    """
    df_join = reduce(lambda left, right: pd.merge(left, right, on=on, how=how),
                     df_list,
                     df_initial)
    return df_join


def explode_list_column(df, column, filling_value, renaming_func=identity_func, pre_processing_func=identity_func,
                        post_processing_func=identity_func):
    """

    Args:
        df (DataFrame):
        column (str):
        filling_value (Any):
        renaming_func (Callable):
        pre_processing_func (Callable):
        post_processing_func (Callable):

    Returns:
        DataFrame:
    """
    pivot = (df[column]
             .apply(pre_processing_func)
             .apply(pd.Series)
             .fillna(filling_value, inplace=False)
             .rename(columns=renaming_func, inplace=False)
             .apply(post_processing_func)
             )
    return pivot


def enrich_with_simple_time_features(df, timestamp_key):
    """

    Args:
        df (DataFrame):

    Returns:
        DataFrame:
    """
    df_copy = pd.DataFrame(df.copy())
    # Adding simple time based features
    df_copy['MONTH'] = df_copy[timestamp_key].apply(lambda x: x.month)
    df_copy['WEEK'] = df_copy[timestamp_key].apply(lambda x: x.week)
    df_copy['WEEKEND'] = df_copy[timestamp_key].apply(lambda x: 1 if x.weekday() >= 5 else 0)
    df_copy['WEEKDAY'] = df_copy[timestamp_key].apply(lambda x: x.weekday())
    df_copy['HOUR'] = df_copy[timestamp_key].apply(lambda x: x.hour)
    return df_copy


# TODO add keys to not lag
def enrich_with_lag_information(df, timestamp_col, subject_col, lags=None, verbose=False):
    """

    Args:
        df (DataFrame):
        lags (list[int]): list of int to shift
        verbose (bool):

    Returns:
        DataFrame:
    """
    if lags is None:
        lags = [1]

    assert len(lags) > 0, "No lags requested ({}), what do you want from me?".format(lags)

    df_copy = pd.DataFrame(df.copy())
    df_with_target_sorted = df_copy.sort_values(by=[subject_col, timestamp_col])

    lag_result = {}
    for lag in lags:
        lag_result[lag] = pd.DataFrame(pd.concat([
                                                     group
                                                 .set_index(timestamp_col)
                                                 .shift(lag)
                                                 .reset_index() for name, group in
                                                     df_with_target_sorted.groupby(subject_col)
                                                     ])).rename(
            columns=lambda x: x + '_LAG_{}'.format(lag) if x not in [timestamp_col, subject_col] else x,
            inplace=False)

    if verbose:
        for k, v in lag_result.items():
            print("Lag", k)
            print(v.info(memory_usage='deep', verbose=False), "\n")
        print("")

    # Merge all the lags
    df_final = join_multiple(df_copy, lag_result.values(), on=[subject_col, timestamp_col])

    # Remove useless columns
    useful_columns_raw = list(set(df_final.columns.tolist()))

    useful_columns = [x for x in useful_columns_raw
                      if not all(sub in x for sub in [subject_col, 'LAG'])
                      and not all(sub in x for sub in [timestamp_col, 'LAG'])
                      # and not all(sub in x for sub in [MONTH, 'LAG'])
                      # and not all(sub in x for sub in [WEEKEND, 'LAG'])
                      # and not all(sub in x for sub in [WEEKDAY, 'LAG'])
                      # and not all(sub in x for sub in [WEEK, 'LAG'])
                      # and not all(sub in x for sub in [HOUR, 'LAG'])
                      # and not all(sub in x for sub in ['MINUTE', 'LAG'])
                      # and not all(sub in x for sub in ['TARGET', 'LAG'])
                      ]

    return df_final[useful_columns]


def add_target(df, timestamp_col, subject_col, delta, target_col='STOP_TYPE_PRESENCE_230', verbose=False):
    """

    Args:
        df (DataFrame):
        delta (timedelta):
        target_col (str):
        verbose (bool):

    Returns:
        DataFrame, str:
    """
    # Columns for the time join
    time_unit_forward = 'time_unit_forward'
    df_target = df.assign(time_unit_forward=lambda x: x[timestamp_col] - delta, axis=1)

    df_to_merge = df_target[[target_col, time_unit_forward, subject_col]]

    target = target_col + '_TARGET'
    df_to_merge.columns = [target, timestamp_col, subject_col]

    df_with_target = pd.merge(df, df_to_merge, on=[timestamp_col, subject_col])

    if verbose:
        print("Null situation:\n", df_with_target.notnull().all())
        print("")
        print("Micro stop presence distribution: [n^]")
        print(Counter(df_with_target[target]))
        print("")
        print("Micro stop presence: [%]")
        print(Counter(df_with_target['STOP_TYPE_PRESENCE_230'])[1] / float(
            sum(Counter(df_with_target['STOP_TYPE_PRESENCE_230']).values())))
        print("")

    return df_with_target, target


def under_sampling(train, target=None, frac=0.66, target_to_under_sample=0, verbose=False):
    """

    Args:
        train (DataFrame):
        target (str):
        frac (float):
        target_to_under_sample (int):
        verbose (bool):

    Returns:
        DataFrame
    """
    if target is None:
        targets_possible = [x for x in train.columns if 'TARGET' in x]
        if len(targets_possible) != 1:
            raise ValueError("Not a single target found... {}".format(targets_possible))
        else:
            target = targets_possible[0]

    # Under-sampling 0 data
    train_0, train_1 = train[train[target] == 0], train[train[target] == 1]
    if target_to_under_sample == 0:
        train = shuffle(pd.concat([train_0.sample(frac=frac, random_state=123), train_1]))
    elif target_to_under_sample == 1:
        train = shuffle(pd.concat([train_1.sample(frac=frac, random_state=123), train_0]))
    else:
        raise ValueError("Target value '{}' not supported".format(target_to_under_sample))

    if verbose:
        print("0 vs 1 length:\n", len(train_0), len(train_1))
        print("Under-sampled train length:", len(train))
    return train
