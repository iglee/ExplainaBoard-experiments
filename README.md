# ExplainaBoard-experiments
for keeping track of experiments done with ExplanaBoard

## Summary of scripts
- `src/process_wmt21reports.py`: organize the json reports from explainaboard into data points with metrics, also calculated URIEL distances
- `src/process_wmt21train.py`: organize the training data from WMT21 into data points with data size, type token ratio, ttr distance, and subword tokenization (subword not implemented yet).
- `src/linear_regression.py`: helper functions for linear regression. 
    - builds regression pipelines from polynomial or simple regression, (basis expansion can be added too, but not added yet.)
    - trains pipelines using bootstrapping, 
    - get feature importances
    - prints results (MSE and R2).
- 
- `sample_data`: for now, I have a `pkl` of a data frame to be used for regression related models.
- `notebooks/linear-regression-analysis.ipynb`: notebook containing results/plots/analysis so far, related to regression models. mostly linear regression was explored, but I tried out SVM and GPR as non-linear examples.