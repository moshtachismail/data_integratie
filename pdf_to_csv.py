import tabula
from tabula.io import read_pdf


def inlezen():
    df = tabula.read_pdf("PGPC-3.pdf", pages = "all")[0]
    tabula.convert_into("PGPC-3.pdf", "patient3.csv", output_format="csv", pages='all')
    print(df)


def main():
    inlezen()

main()
