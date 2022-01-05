from pathlib import Path
import abir

DEBUG = True


BASE_DIR = Path(__file__).resolve().parent.parent
abir.load(base_dir=BASE_DIR, conf_module='testsuites.conf_module')
