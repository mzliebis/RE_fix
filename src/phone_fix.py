import pandas as pd
from pathlib import Path


def format_phone_file(df):

    print(f"pre formatted file rows: {df.shape[0]}")

    # remove nan values
    mask = df['CnPh_1_01_Phone_number'].isna()
    df = df[~mask]

    print(f"removed nan values file rows: {df.shape[0]}")

    # remove correctly formatted numbers
    #mask = df['CnPh_1_01_Phone_number'].str.fullmatch(r'\d{3}-\d{3}-\d{4}')
    mask = df['CnPh_1_01_Phone_number'].str.fullmatch(r'\(\d{3}\) \d{3}-\d{4}')
    df = df[~mask]


    # clean
    df['CnPh_1_01_Phone_number'] = (df['CnPh_1_01_Phone_number'].str.replace("(", "").
                                    str.replace(")", "").
                                    str.replace("-", "").
                                    str.replace(" ", "")
                                    )

    mask_1 = df['CnPh_1_01_Phone_number'].str.len() == 11
    mask_2 =  df['CnPh_1_01_Phone_number'].str[0] == "1"
    mask = mask_1 & mask_2

    df.loc[mask, 'CnPh_1_01_Phone_number'] = df['CnPh_1_01_Phone_number'].str[1:]

    #df['CnPh_1_01_Phone_number'] = df['CnPh_1_01_Phone_number'].astype(str)
    #df['CnPh_1_01_Phone_number'] = df['CnPh_1_01_Phone_number'][0:4]

    df['CnPh_1_01_Phone_number'] = ("(" +df['CnPh_1_01_Phone_number'].str[0:3] + ")" +
                                    " " +df['CnPh_1_01_Phone_number'].str[3:6] + "-" +
                                    df['CnPh_1_01_Phone_number'].str[6:10])









    print(f"remove correct format row: {df.shape[0]}")




    # mask = df['CnPh_1_01_Phone_type'] == "Cell Phone"
    # df=df[mask]
    #
    # print(f"removed cell phone type rows: {df.shape[0]}")







    # df = df.astype(str)
    return df


def format_for_re_import(df):

    df = df.rename(columns={'CnBio_Import_ID': 'ImportID',
                            'CnPh_1_01_Import_ID': 'PhoneImpID',
                            'CnPh_1_01_Phone_number': 'PhoneNum',
                            'CnPh_1_01_Phone_type': 'PhoneType'
                            })



    return df[['ImportID', 'PhoneImpID', 'PhoneNum' , 'PhoneType']]






if __name__ == '__main__':

    path_in = Path(Path.cwd().parent / "data" )
    path_out = Path(Path.cwd().parent / "out" )

    fn = "re_phone_fix.CSV"
    fn_out = "phone_upload.CSV"
    fn_test_out = "test_" + fn_out

    re = pd.read_csv(Path(path_in / fn))
    re = format_phone_file(re)
    re = format_for_re_import(re)

    print(re.head(10).to_markdown())

    re.to_csv(Path(path_out / fn_out), index=False)

    test = re.head(10)
    test.to_csv(Path(path_out / fn_test_out), index=False)
