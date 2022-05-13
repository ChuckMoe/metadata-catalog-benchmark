import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_PATH = Path('../volume/timing').absolute()


def load_csv(filepath: Path) -> pd.DataFrame:
    file_as_list = filepath.name.split('.')
    catalogue = file_as_list[0].title()
    schema = file_as_list[1].title()
    df = pd.read_csv(filepath)
    df['Catalogue'] = catalogue
    df['Schema'] = schema
    return df


def create_plot(df: pd.DataFrame, out: Path, title: str = None):
    fig = px.box(df, x='Catalogue', y='Elapsed Time', color='Schema', title=title)
    fig.update_yaxes(tick0=0.0)
    fig.write_image(file=out, format='png')


def create_plots_step_size(dirpath: Path):
    df = pd.DataFrame()
    for file in dirpath.iterdir():
        if file.is_file() and '.csv' == file.suffix:
            df = pd.concat([df, load_csv(file)])

    step_size = dirpath.name
    schema_size = dirpath.parent.name
    out = BASE_PATH / 'datasize_{}-steps_{}.png'.format(schema_size, step_size)
    create_plot(df, out, title='{} Schema Entries - {} Step size'.format(schema_size, step_size))


def create_plots_dataset_size(dirpath: Path):
    if not dirpath.is_dir():
        return

    for folder_step_size in dirpath.iterdir():
        create_plots_step_size(folder_step_size)


def create_plots_timing():
    for folder_data_size in BASE_PATH.iterdir():
        create_plots_dataset_size(folder_data_size)


if __name__ == '__main__':
    create_plots_timing()
