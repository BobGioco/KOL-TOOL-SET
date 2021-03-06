from lib.XML_Parser import table
import os, sys
import pandas as pd
import xml.etree.ElementTree as et

dir_path = os.path.dirname(os.path.realpath('.'))
data_path=os.path.join(sys.path[1],'data')

if __name__=="__main__":
    print(len(sys.argv))
    exit()
    if len(sys.argv)>1:
        xml_path=sys.argv[1]
    else:
        xml_path=os.path.join(data_path,'pubmed_data_out_full.xml')
    tree = et.parse(xml_path)
    root = tree.getroot()
    xl = pd.ExcelFile(os.path.join(data_path,"MetaDataConfig.xlsx"))
    for sheet in xl.sheet_names:
        if sheet!="_AuthorList":
            df=xl.parse(sheet)
            dct=table(df,root).get_table()
            output_df=pd.DataFrame(dct)
            if sheet=="AbstractList":
                output_df.dropna(axis=0,how='all',subset=['Text', 'Label'],inplace=True)
                output_df['Abstract_text']=output_df['Label'].apply(lambda x: x + ": " if not x is None else "") + output_df['Text']
                output_df=output_df.groupby(['PMID','Type'])['Abstract_text'].apply(' '.join).reset_index()
                output_df.rename(columns={"Abstract_text":"Text"},inplace=True)
            elif sheet=="AuthorList":
                output_df['AuthorType']=output_df['AuthorType'].apply(lambda x: 'authors' if x is None else x)

            output_df.to_csv(os.path.join(data_path,'tables',sheet + ".csv"),sep='|',index=False)
