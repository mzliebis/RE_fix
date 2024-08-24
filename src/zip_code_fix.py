import pandas as pd
from pathlib import Path


def format_zip_file(df):

    df = df.astype(str)
    return df


def select_zip_length_4_add_zero(df):

    df = df.copy()
    print(f"zip length 4 pre:{df.shape[0]}")
    mask = (df['CnAdrPrf_ZIP'].str.len() == 4)
    df = df[mask]
    df['CnAdrPrf_ZIP'] = df['CnAdrPrf_ZIP'].str.zfill(5)
    print(f"zip length 4 post:{df.shape[0]}")

    return df


def format_for_re_import(df):

    df = df.rename(columns={'CnBio_ID': 'ConsID',
                            'CnAdrPrf_Addrline1': 'AddrLines',
                            'CnAdrPrf_City': 'AddrCity',
                            'CnAdrPrf_State': 'AddrState',
                            'CnAdrPrf_ZIP': 'AddrZIP'
                            })

    df['PrefAddr'] = "Yes"

    return df[['ConsID', 'PrefAddr',  'AddrLines',  'AddrCity', 'AddrState', 'AddrZIP']]






if __name__ == '__main__':

    path_in = Path(Path.cwd().parent / "data" )
    path_out = Path(Path.cwd().parent / "out" )

    fn = "zip_fix_08_13_2024.CSV"
    fn_out = "zip_upload.CSV"
    fn_test_out = "test_" + fn_out

    re = pd.read_csv(Path(path_in / fn),  encoding='latin1')


    re = format_zip_file(re)
    re = select_zip_length_4_add_zero(re)



    #
    #
    re = format_for_re_import(re)

    print(re.head(10))



    re.to_csv(Path(path_out / fn_out), index=False)

    test = re.head(1)
    test.to_csv(Path(path_out / fn_test_out), index=False)
