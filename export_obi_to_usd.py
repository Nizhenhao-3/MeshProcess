import glob
import argparse



full_path_lst = glob.glob(cfg["data"]["input_template"])
prefix = cfg["data"]["input_template"].split("*")[0]
suffix = cfg["data"]["input_template"].split("**")[-1]
obj_lst = [p.replace(prefix, "").replace(suffix, "") for p in full_path_lst]







if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_template', type=str, required=True)
    parser.add_argument('-o', '--output_template', type=str, required=True)

    args = parser.parse_args()
    
