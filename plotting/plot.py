from pathlib import Path

import pandas as pd
import plotly.express as px

BASE_PATH = Path(__file__).absolute().parent.parent / 'output/timing'


def load_csv(filepath: Path) -> pd.DataFrame:
    file_as_list = filepath.name.split('.')
    catalogue = file_as_list[0].title()
    schema = file_as_list[1].title()
    df = pd.read_csv(filepath)
    df['Catalogue'] = catalogue
    df['Schema'] = schema
    return df


def _create_plot(df: pd.DataFrame, out: Path, suffix: str, title: str):
    fig_upload = px.box(df, x='Catalogue', y='{} - Elapsed Time'.format(suffix), color='Schema', title=title)
    fig_upload.update_yaxes(tick0=0.0)
    fig_upload.write_image(file='{}.{}.png'.format(out, suffix), format='png')


def create_plot(df: pd.DataFrame, out: Path, title: str = None):
    _create_plot(df, out, 'upload', title)
    _create_plot(df, out, 'query_zero', title)
    _create_plot(df, out, 'query_one', title)
    _create_plot(df, out, 'query_some', title)
    _create_plot(df, out, 'query_all', title)


def create_plots_step_size(dirpath: Path):
    df = pd.DataFrame()
    for file in dirpath.iterdir():
        if file.is_file() and '.csv' == file.suffix:
            df = pd.concat([df, load_csv(file)])

    step_size = dirpath.name
    schema_size = dirpath.parent.name
    out = BASE_PATH / 'datasize_{}-steps_{}'.format(schema_size, step_size)
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
