
import numpy as np

def prepare_X(df, base, categories):
    df = df.copy()
    features = base.copy()

    df["age"] = 2017 - df["year"]
    features.append("age")

    for v in [2, 3, 4]:
        df["num_doors_%s" % v] = (df["number_of_doors"] == v).astype("int")
        features.append("num_doors_%s" % v)

    for c, values in categories.items():
        for v in values:
            df["%s_%s" % (c, v)] = (df[c] == v).astype("int")
            features.append("%s_%s" % (c, v))

    df_num = df[features]
    df_num = df_num.fillna(0)
    return df_num.values
