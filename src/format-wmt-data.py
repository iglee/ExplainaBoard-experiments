import glob, os
import pandas as pd


def get_files(input_dir):
    """
    get all files in a given directory as a list
    """
    return list(map(os.path.basename, glob.glob(input_dir + "/*")))


def generate_formatted_files(input_dir, label_dir, output_root_dir, formatted_dir):
    """
    given input, label, and output directories, format the files for ExplainaBoard experiments
    """
    # input_files = get_files(input_dir)
    ref_files = get_files(label_dir)

    for file in ref_files:
        task, lang_pair, _, _, _ = file.split(".")
        # for now, i'll default to ref-A
        labels = open(label_dir + "/" + file, "r").read().splitlines()

        input_file = ".".join([task, lang_pair, "src", lang_pair.split("-")[0]])
        inputs = open(input_dir + "/" + input_file, "r").read().splitlines()

        output_dir = output_root_dir + "/{}/{}".format(task, lang_pair)
        output_files = get_files(output_dir)
        for hyp_file in output_files:
            outputs = open(output_dir + "/" + hyp_file).read().splitlines()
            team_name = hyp_file.split(".")[-2]
            formatted_file = ".".join([task, lang_pair, team_name])

            # print(len(inputs) == len(outputs) == len(labels))
            data = {"inputs": inputs, "labels": labels, "outputs": outputs}
            pd.DataFrame(data).to_csv(
                formatted_dir + "/" + formatted_file + ".tsv", sep="\t", header=False
            )


if __name__ == "__main__":
    input_dir = "../data/wmt21/sources"
    output_root_dir = "../data/wmt21/system-outputs"
    label_dir = "../data/wmt21/references"
    formatted_dir = "../data/wmt21/formatted"

    generate_formatted_files(input_dir, label_dir, output_root_dir, formatted_dir)
