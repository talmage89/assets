"""Physical attachment checks, independent of export serialization and motion."""
import runpy
from pathlib import Path
CONTACTS=runpy.run_path(str(Path(__file__).with_name('config.py')))['CONTACTS']+[
('Fixed hinge anchor','Bent galvanized shell',.0002),
('Fixed hinge anchor','Fixed hinge bracket',.0002),
('Fixed hinge bracket','Fixed hinge pin',.0002),
('Fixed hinge anchor.001','Bent galvanized shell',.0002),
('Fixed hinge anchor.001','Fixed hinge bracket.001',.0002),
('Fixed hinge bracket.001','Fixed hinge pin.001',.0002),
('Flag nylon stand-off','Bent galvanized shell',.0002),
('Roof spring catch','Bent galvanized shell',.0005)]
