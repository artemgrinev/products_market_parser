from parsers.okey_parser import ProductOkay
from parsers.vprok_parser import ProductVprok
from data import writer_csv


okey = ProductOkay().start_parser()
vprok = ProductVprok().start_parser()

if __name__ == "__main__":
    writer_csv('okey', okey)
    writer_csv('vprok', vprok)