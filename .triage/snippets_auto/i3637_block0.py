import statsmodels.api as sm

data = sm.datasets.longley.load_pandas().data

properties = ['GNP', 'POP']
specificData = data[properties]

