import pandas as pd
import numpy as np
from copy import deepcopy
from collections import defaultdict

# sklearn imports
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# scipy imports
from scipy.stats import zscore

metrics = ["bleu", "rouge2", "mover_score"]
uriel_features = [
    "genetic",
    "geographic",
    "syntactic",
    "inventory",
    "phonological",
    "featural",
]
all_features = [
    "genetic",
    "geographic",
    "syntactic",
    "inventory",
    "phonological",
    "featural",
    "source_ttr",
    "target_ttr",
    "data_size",
    "ttr_distance",
]


def z_norm_feats(df, feats):
    for f in feats:
        df[f] = zscore(df[f])
    return df


def build_simple_regression_pipeline():
    steps = [("regression", LinearRegression())]
    pipeline = Pipeline(steps=steps)
    return pipeline


def build_polynomial_regression_pipeline(degree):
    steps = [("poly", PolynomialFeatures(degree)), ("regression", LinearRegression())]
    pipeline = Pipeline(steps=steps)
    return pipeline


def train_regression(df_data, reg_pipeline, metrics, feats):

    feats = np.array(feats)
    df = z_norm_feats(df_data, feats)

    reg = reg_pipeline
    reg.fit(df[feats], df[metrics])

    return reg


def bootstrap_train(
    df_data, pipeline, metrics, feats, n_bootstraps=200, sample_size=70
):

    pipelines = []

    for _ in range(n_bootstraps):
        df_sample = df_data.sample(n=sample_size, replace=True)
        sample_pipeline = train_regression(df_sample, pipeline, metrics, feats)
        pipelines.append(deepcopy(sample_pipeline))

    return pipelines


def gather_coefficients(bootstrapped_pipelines, metrics, features):
    # for simple linear regression only

    coefficients = {}

    for m in metrics:
        coefficients[m] = defaultdict(list)

    for p in bootstrapped_pipelines:
        coef_vals = p.named_steps["regression"].coef_

        for i in range(len(metrics)):
            for j in range(len(features)):
                coefficients[metrics[i]][features[j]].append(coef_vals[i][j])
    return coefficients


def feature_importances(model, features):
    # for simple linear regression only

    importances = model.named_steps["regression"].coef_

    # use np indexing to order the feature names to increasing order of importances
    ords = np.flip(np.argsort(importances), axis=1)
    importances = importances[np.array([0, 1, 2])[:, np.newaxis], ords]
    feats_match = np.array(features)[ords]

    ret = {}

    for i, metric in enumerate(metrics):
        ret[metric] = {"features": feats_match[i], "importance_vals": importances[i]}

    return ret


def print_results(model, feats, df):
    test_pred = model.predict(df[feats])
    mse = mean_squared_error(test_pred, df[metrics])
    r2 = r2_score(df[metrics], test_pred)
    print("mse error: {}, r2 score: {}".format(mse, r2))

