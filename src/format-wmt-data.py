import glob, os


def get_files(input_dir):
    """
    get all files in a given directory as a list
    """
    return list(map(os.path.basename, glob.glob(input_dir + "/*")))


def generate_formatted_files(input_dir, label_dir, output_root_dir, formatted_dir):
    """
    given input, label, and output directories, format the files for ExplainaBoard experiments
    """
    input_files = get_files(input_dir)
    ref_files = get_files(label_dir)
    for file in input_files:
        task, lang_pair, _, _ = file.split(".")
        # for now, i'll default to ref-A
        inputs, labels = [], []

        for ref in ["ref-A", "ref-B", "ref-C", "ref-D"]:
            ref_file = ".".join(
                [task, lang_pair, "ref", "ref-A", lang_pair.split("-")[-1]]
            )
            if ref_file in label_dir:
                inputs = open(input_dir + "/" + file, "r").read().splitlines()
                labels = open(label_dir + "/" + ref_file, "r").read().splitlines()
                if len(inputs) == len(labels):
                    break

        output_dir = output_root_dir + "/{}/{}".format(task, lang_pair)

        output_files = get_files(output_dir)

        for hyp_file in output_files:
            outputs = open(output_dir + "/" + hyp_file).read().splitlines()
            team_name = hyp_file.split(".")[-2]
            formatted_file = ".".join([task, lang_pair, team_name])
            with open(formatted_dir + "/" + formatted_file + ".tsv", "w") as f:
                for i in range(len(inputs)):
                    f.write("\t".join([inputs[i], labels[i], outputs[i]]) + "\n")

            f.close()


if __name__ == "__main__":
    input_dir = "../data/wmt21/sources"
    output_root_dir = "../data/wmt21/system-outputs"
    label_dir = "../data/wmt21/references"
    formatted_dir = "../data/wmt21/formatted"

    generate_formatted_files(input_dir, label_dir, output_root_dir, formatted_dir)
