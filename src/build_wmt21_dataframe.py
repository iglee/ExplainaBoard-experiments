from process_wmt21reports import WMT21ReportData
from process_wmt21train import WMT21TrainData
import glob
from os.path import basename
import pandas as pd

moverscore_reports = "../reports/wmt21-04242022-moverscore/"
rouge2_reports = "../reports/wmt21-04242022-rouge2/"
bleu_reports = "../reports/wmt21-04062022/"
train_data_dir = "../data/wmt21-training-sources/"
reference_data_dir = "../data/wmt21-training-references/"

train_set = {}

for file in glob.glob(train_data_dir + "*"):
    data = WMT21TrainData(file)

    train_set[data.dataset + "." + data.langpair + "." + data.language] = {
        "ttr": data.ttr,
        "data_size": data.data_size,
    }

reference_set = {}

for file in glob.glob(reference_data_dir + "*"):
    data = WMT21TrainData(file)

    reference_set[data.dataset + "." + data.langpair + "." + data.language] = {
        "ttr": data.ttr,
        "data_size": data.data_size,
    }

report_set = {}

for file in glob.glob(moverscore_reports + "*"):
    data = WMT21ReportData(file)
    data.get_metrics("mover_score")
    data.get_fine_grained_results("mover_score")
    report_set[data.basename] = data

for file in glob.glob(bleu_reports + "*"):
    base = basename(file)
    data = report_set[base]
    data.get_metrics("bleu", filename=file)
    data.get_fine_grained_results("bleu", filename=file)

for file in glob.glob(rouge2_reports + "*"):
    base = basename(file)
    data = report_set[base]
    data.get_metrics("rouge2", filename=file)
    data.get_fine_grained_results("rouge2", filename=file)

total_data = []
missing_train_data = []

for report in report_set.values():

    try:
        datum = {
            "dataset": report.dataset,
            "langpair": report.langpair,
            "model": report.model,
        }
        for k, v in report.uriel_distances.items():
            datum[k] = v

        for k, v in report.metrics.items():
            datum[k] = v

        for k, v in report.fine_grained_results.items():
            for k1, v1 in v.items():
                datum[k + "|" + k1] = v1

        source_key = ".".join([report.dataset, report.langpair, report.source_lang_2])
        source_data = train_set[source_key]

        target_key = ".".join([report.dataset, report.langpair, report.target_lang_2])
        target_data = reference_set[target_key]

        datum["source_ttr"] = source_data["ttr"]
        datum["target_ttr"] = target_data["ttr"]
        datum["data_size"] = source_data[
            "data_size"
        ]  # target_data["data_size"] == source_data["data_size"]

        ttr_ratio = source_data["ttr"] / target_data["ttr"]
        ttr_distance = (1 - ttr_ratio) ** 2
        datum["ttr_distance"] = ttr_distance

        total_data.append(datum)

    except:
        missing_train_data.append(report.basename)

df = pd.DataFrame(total_data).dropna()
df.to_pickle("../data/wmt21_processed_data_fine_grained.pkl")
