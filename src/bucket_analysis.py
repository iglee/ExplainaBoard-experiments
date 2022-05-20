import scipy.stats as stats
import math
import numpy as np

# helper functions for bucketed feature analysis


def get_rank_by_metric(df, metric):
    df = df.sort_values(by=[metric], ascending=False).reset_index(drop=True)
    df.index = df.index.set_names(["{}_rank".format(metric)])
    df = df.reset_index()
    return df


def get_column_name(df, metric, fine_grained_feature):
    return df.filter(regex=("{}.*{}").format(metric, fine_grained_feature)).columns[-1]


def column_selector(df, metric, fine_grained_feature, idx_bucket):
    colname = get_column_name(df, metric, fine_grained_feature)
    try:
        return df[colname].apply(lambda x: x[list(x.keys())[idx_bucket]])
    except:
        # most likely due to idx_bucket out of range
        pass


def performances_by_bucket(df, metric, fine_grained_feature, bucket):
    return column_selector(df, metric, fine_grained_feature, bucket).apply(
        lambda x: x[0]
    )


def delta_expected_perf(df, metric, fine_grained_feature, bucket):
    col = column_selector(df, metric, fine_grained_feature, bucket).apply(
        lambda x: x[0]
    )

    return abs(df["{}_rank".format(metric)] - (-1 * col).argsort())


def get_mode_model(df_performances):
    just_model_idxs = np.array(
        [
            x
            for x in df_performances.values.flatten()
            if isinstance(x, (float, int)) and not math.isnan(x)
        ]
    )

    return stats.mode(just_model_idxs)
