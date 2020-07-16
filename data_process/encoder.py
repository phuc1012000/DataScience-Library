from pandas import pd


class encoder:
    def __init__(self, cols, trn_df, tst_df=None):

        self.cols,
        self.trn_df,
        self.tst_df = self._checking_error(cols, trn_df, tst_df)

    def _checking_error(self, cols, trn_df, tst_df):
        # checking columns
        if isinstance(cols, str):
            cols = [cols]
        # check if list or not
        else:
            if not self._iterable(cols):
                raise Exception("cols is iterable or one string")

        self._check_dataframe(cols, trn_df)

        if tst_df is not None:
            self._check_dataframe(cols, tst_df)

        return cols, trn_df, tst_df

    def _check_dataframe(self, cols, df):
        if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
            for col in cols:
                if col not in df.columns:
                    raise Exception(
                        "cols is not in  DataFrame \
                                     follow input order"
                    )
        else:
            raise Exception(
                "DataFrame follow input order is not \
                            pd.DataFrame or pd.Series"
            )

    def _iterable(self, obj):
        try:
            iter(obj)
            return True

        except TypeError:
            return False

    def _fit(self, fit):
        if fit == "all":
            temp = pd.concat([self.trn_df[self.cols], self.tst_df[self.cols]])
        if fit == "trn_df":
            temp = self.trn_df.copy()
        else:
            raise Exception('fit only "all" or "trn_df"')
        return temp

    def freq_encoding(
        self, fit="trn_df", transform="all",
    ):

        for df in self.dfs:
            for col in self.cols:
                col_freq = col + "_freq"
                freq = self.train_df[self.col].value_counts()
