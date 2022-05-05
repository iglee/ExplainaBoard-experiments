import glob
import os
import json
import pycountry
import lang2vec.lang2vec.lang2vec as l2v  # package build failed so git cloned
import time

seen_distance = {}  # querying uriel distances take a while


class WMT21ReportData:
    def __init__(self, filename):
        self.filename = filename
        self.basename = os.path.basename(filename)
        self.dataset, self.langpair, self.model, _ = self.basename.split(".")
        self.source_lang_2, self.target_lang_2 = self.langpair.split("-")
        self.source_lang_3 = self.iso2_to_3(self.source_lang_2)
        self.target_lang_3 = self.iso2_to_3(self.target_lang_2)
        self.data = {filename: self.read_file(filename)}
        self.metrics = {}
        self.uriel_distances = {}
        self.get_uriel_distances()

    def iso2_to_3(self, iso2_language_code):
        return pycountry.languages.get(alpha_2=iso2_language_code).alpha_3

    def iso2_to_full(self, iso2_language_code):
        return pycountry.languages.get(alpha_2=iso2_language_code).name

    def read_file(self, filename):
        try:
            f = open(filename)
            data = json.load(f)
            return data
        except:  # there are ~ 5 empty file errors
            pass

    def get_metrics(self, metric, filename=None):
        # get metric values of interest from the original dataset or from other reports
        # had to generate individual reports for individual metrics due to some errors (mostly client disconnected error)

        if filename:
            data = self.read_file(filename)
            self.data[filename] = data
        else:
            data = self.data[self.filename]

        if data:
            metric_value = data["results"]["overall"][metric]["value"]
            self.metrics[metric] = metric_value

    def get_uriel_distances(self):

        if self.langpair in seen_distance.keys():
            self.uriel_distances = seen_distance[self.langpair]
        else:
            for dist_type in [
                "genetic",
                "geographic",
                "syntactic",
                "inventory",
                "phonological",
                "featural",
            ]:
                self.uriel_distances[dist_type] = l2v.distance(
                    dist_type, self.source_lang_3, self.target_lang_3
                )

            seen_distance[self.langpair] = self.uriel_distances
            seen_distance[
                self.target_lang_2 + "-" + self.source_lang_2
            ] = self.uriel_distances  # distance from A to B == distance from B to A


if __name__ == "__main__":
    report_dir = "../reports/wmt21-04242022-moverscore"

    start = time.perf_counter()
    for f in glob.glob(report_dir + "/*"):
        r = WMT21ReportData(f)
        r.get_metrics("mover_score")

    print(
        "took {} seconds.".format(time.perf_counter() - start)
    )  # around a minute for full wmt21 reports.
