import argparse
import inspect
import shutil
import sys
import os
import pandas as pd
import pickle

import boto3
from botocore.exceptions import NoCredentialsError

from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier


def prepare_parser():
    parser = argparse.ArgumentParser(description="The utility helps data "
                                                 "scientists train models.")

    parser.add_argument('model', type=str, help='Model name', choices=[
        'decision_tree', 'forest', 'gradient_boosting', 'PCA'])

    parser.add_argument('inp_path', type=str,
                        help='Input dataset.')

    parser.add_argument('out_dir', type=str,
                        help='Place where trained model will be stored.')

    parser.add_argument('--compression', type=str,
                        help='Compression algorithm',
                        choices=['tar.gz', 'tar.bz2', 'zip'])

    parser.add_argument('--max_depth', type=str,
                        help='The maximum depth of the tree.')

    parser.add_argument('--min_samples_leaf', type=str,
                        help='The minimum number of samples required to be'
                             ' at a leaf node.')

    parser.add_argument('--min_samples_split', type=str,
                        help=' The minimum number of samples required to split'
                             ' an internal node.')

    parser.add_argument('--learning_rate', type=str,
                        help='Boosting learning rate.')

    parser.add_argument('--n_estimators', type=str,
                        help='The number of trees in the forest.')

    parser.add_argument('--n_components', type=str,
                        help=' Number of components to keep.')

    parser.add_argument('--target_col', type=str, default='y',
                        help='Target variable. By default "y".')
    return parser


def process_file(files, available_extensions, out_dir, model, args,
                 target_col, compression):
    inp_path = files[0]
    correct_inp = inp_path.endswith(available_extensions)
    if correct_inp:
        extension = inp_path.rsplit('.', 1)[1]

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    dir_exists = os.path.isdir(out_dir) or out_dir.startswith('https:')

    if correct_inp and dir_exists:
        run_save_model(extension, files, model, args, out_dir, target_col,
                       compression)
    else:
        print('error')
        sys.exit()


def run_save_model(ext, files, model, args, out_dir, target_col, compression):
    models_dict = {
        'decision_tree': DecisionTreeClassifier,
        'gradient_boosting': XGBClassifier,
        'forest': RandomForestClassifier,
        'PCA': PCA,
    }
    X, y = get_data(files, ext, target_col)
    Model = models_dict[model]
    to_number = lambda x: float(x) if '.' in x else int(x)
    ml_args = {k: to_number(v) for k, v in args.__dict__.items() if k in
               inspect.getargspec(Model)[0] and v is not None}
    cls = Model(**ml_args)
    cls.fit(X, y)

    with open(out_dir + '/' + model, 'wb') as f:
        pickle.dump(cls, f)
        if not os.path.isdir(out_dir):
            if not os.path.isdir(out_dir):
                upload_to_aws(cls, 'bucket_name', out_dir)


def get_data(files, ext, target_col):
    reader_dict = {
        'csv': pd.read_csv,
        'json': pd.read_json,
        'parquet': pd.read_parquet,
    }

    Reader = reader_dict[ext]

    df_all = pd.concat([Reader(ifile_path) for ifile_path in files],
                       ignore_index=True)

    y = df_all.pop(target_col)
    X = df_all

    return X, y


ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXXX'
SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'


# S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format('yourbucketname')


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def main():
    available_extensions = ('.csv', '.parquet', '.json', '.tar.gz', '.tar.bz2',
                            '.zip')
    parser = prepare_parser()
    args = parser.parse_args()

    model = args.model
    inp_path = args.inp_path
    out_dir = args.out_dir
    compression = args.compression
    print(compression)
    target_col = args.target_col

    # If the input is archive
    if inp_path.endswith(available_extensions[-3:]):
        shutil.unpack_archive(inp_path, 'tmp')

        # If archive contains a file
        if not os.path.isdir('tmp/'):
            files = ['tmp/' + x for x in os.listdir('tmp')]

        # If archive contains a directory
        else:
            files = ['tmp/' + os.listdir('tmp')[0] + '/' + x for x in
                     os.listdir(os.listdir('tmp')[0])]
    else:
        # If inp is file
        if not os.path.isdir(inp_path):
            files = [inp_path]
        # If inp is directory
        else:
            files = [inp_path + '/' + x for x in os.listdir(inp_path)]

    # Start processing file
    process_file(files, available_extensions, out_dir, model, args,
                 target_col, compression)

    if os.path.exists('tmp'):
        shutil.rmtree('tmp')


if __name__ == '__main__':
    main()
