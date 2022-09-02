import os
import sys
import torch


if __name__ == "__main__":
    d4j_version = sys.argv[1]
    bug_version = sys.argv[2]
    fl_setting = sys.argv[3]
    BEAM_35 = int(sys.argv[4].strip())
    BEAM_single = int(sys.argv[5].strip())
    use_gpu = torch.cuda.is_available()

    nmt_origin_dir = os.path.abspath("../nmt_model/origin_onmt/")
    nmt_combine_dir = os.path.abspath("../nmt_model/joint_inference/")
    check_point_dir = os.path.join(nmt_origin_dir, "check_point/")
    src_path = os.path.abspath("../parsed_data/d4j_{}/{}/{}/completion_info/src.txt"
                               .format(d4j_version, fl_setting, bug_version))

    for part in ["copy_35", "copy_single"]:
        current_beam = BEAM_35 if part.endswith("35") else BEAM_single
        cmd = "cd {} && python3 translate.py -model {} -src {} "\
              "-output {} -batch_size 1 -beam_size {} -n_best {} {}"\
            .format(nmt_origin_dir, os.path.join(check_point_dir, part, "saved_model.pt"),
                    src_path, os.path.join(nmt_origin_dir, "d4j_result/{}.txt".format(part)), current_beam, current_beam, "-gpu 0" if use_gpu else "")
        os.system(cmd)

    for part in ["combine_35", "combine_single"]:
        current_beam = BEAM_35 if part.endswith("35") else BEAM_single
        copy_model_dir = "copy_35" if part.endswith("35") else "copy_single"
        nocopy_model_dir = "nocopy_35" if part.endswith("35") else "nocopy_single"
        cmd = "cd {} && python3 translate.py -model {} -model_tmp {} -src {} "\
              "-output {} -batch_size 1 -beam_size {} -n_best {} {}"\
            .format(nmt_combine_dir, os.path.join(check_point_dir, copy_model_dir, "saved_model.pt"),
                    os.path.join(check_point_dir, nocopy_model_dir, "saved_model.pt"),
                    src_path, os.path.join(nmt_combine_dir, "d4j_result/{}.txt".format(part)), current_beam, current_beam, "-gpu 0" if use_gpu else "")
        os.system(cmd)
