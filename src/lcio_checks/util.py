import configparser
import datetime
import logging
import os

import matplotlib
import pandas as pd
from IPython.display import HTML, Image, display

logger = logging.getLogger(__name__)


def button_hide_code():
    """Hide code cells in jupyterlab by the click of a button.

    https://github.com/jupyterlab/jupyterlab/issues/7120#issuecomment-541565837
    """
    return HTML(
        """
        <script src='//code.jquery.com/jquery-3.3.1.min.js'></script>
        <script>
            code_show=false;
            function code_toggle() {
                if (code_show){
                    $('div.input').hide();
                    $('div .jp-CodeCell .jp-Cell-inputWrapper').hide();
                } else {
                    $('div.input').show();
                    $('div .jp-CodeCell .jp-Cell-inputWrapper').show();
                }
                code_show = !code_show
            }
            $( document ).ready(code_toggle);
        </script>
        <form action="javascript:code_toggle()">
            <input type="submit" value="Code hide/show">
        </form>"""
    )


def _read_config():
    """Looks for a [lcio_checks] of setup.cfg in CWD or its parents."""
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "setup.cfg")
    assert config.read(config_file)  # Version shipped with the package.

    dir_name = os.getcwd()
    filesystem_root = os.path.abspath(os.sep)
    while dir_name != filesystem_root:
        config_file = os.path.join(dir_name, "setup.cfg")
        if os.path.exists(config_file):
            config.read(config_file)
            if "lcio_checks" in config.sections():
                break
        dir_name = os.path.dirname(dir_name)
    config = config["lcio_checks"]
    config.path = config_file
    return config


def _configure_logging(verbose=True, log_folder=os.path.curdir):
    FORMAT = "[%(levelname)s:%(name)s] %(message)s"
    if verbose:
        log_level = "INFO"
        logging.basicConfig(format=FORMAT, level=log_level)
        log_file = os.path.join(log_folder, "lcio_checks.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(fmt=logging.Formatter(fmt=FORMAT))
        logging.getLogger().addHandler(file_handler)  # Added to the root logger.
        time_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        logger.info(
            " ".join(
                [
                    f"Logging with level {log_level}.",
                    f"Appended to {log_file} at {time_now}.",
                ]
            )
        )
    else:
        logging.basicConfig(format=FORMAT, level="WARNING")


def get_config(config=None):
    """Looks for a [lcio_checks] field in a parent directories setup.cfg file."""
    if config is None:
        config = _read_config()

    if not os.path.isabs(config["img_cache"]):
        config["img_cache"] = os.path.join(
            os.path.dirname(config.path), config["img_cache"]
        )
    if not os.path.exists(config["img_cache"]):
        os.mkdir(config["img_cache"])

    _configure_logging(config.getboolean("verbose"), config["img_cache"])
    if config.getboolean("verbose"):
        display(button_hide_code())

    # Additional validity checks.
    os.path.isdir(config["data_dir"])
    config.getint("img_dpi")
    config["img_ext"]

    return config


config = get_config()


def _load_image(fig_path):
    img = Image(filename=fig_path, retina=True)
    display(img)
    return img


def load_or_make(names, img_dpi=config.getint("img_dpi")):
    _PNG = ".png"
    full_names = [name + _PNG if not name.endswith(".csv") else name for name in names]
    full_names = [os.path.join(config["img_cache"], name) for name in full_names]

    def decorator(fct):
        def wrapper(*args, **kwargs):
            redo = kwargs.pop("redo", False)
            redo = redo or config.getboolean("img_redo_all", False)
            no_save = kwargs.pop("no_save", False)
            if no_save and not redo:
                raise Exception(f"{no_save=} requires redo=False.")
            if redo or not all([os.path.exists(name) for name in full_names]):
                if not no_save:
                    backend_ = matplotlib.get_backend()
                    matplotlib.use("Agg")
                all_returns = fct(*args, **kwargs)
                if no_save:
                    return all_returns
                if len(all_returns) != len(full_names):
                    raise Exception(f"{len(all_returns)=} != {len(full_names)=}")
                for ret_obj, save_path in zip(all_returns, full_names):
                    if isinstance(ret_obj, matplotlib.figure.Figure):
                        logger.info(f"Figure saved to {save_path}.")
                        ret_obj.savefig(save_path, dpi=img_dpi)
                        _load_image(save_path)
                        try:
                            assert save_path.endswith(_PNG)
                            ret_obj.savefig(
                                save_path[:-4] + config["img_ext"], dpi=img_dpi
                            )
                        except ValueError as ve:
                            logger.exception(ve)
                    else:
                        logger.info(f"DataFrame saved to {save_path}.")
                        display(HTML(ret_obj.to_html()))
                        ret_obj.to_csv(save_path)
                matplotlib.use(backend_)
            else:
                all_returns = []
                for obj_path in full_names:
                    if obj_path.endswith(".csv"):
                        logger.info(f"DataFrame loaded from {obj_path}.")
                        _df = pd.read_csv(obj_path, index_col=0)
                        display(HTML(_df.to_html()))
                        all_returns.append(_df)
                    else:
                        logger.info(f"Figure loaded from {obj_path}.")
                        all_returns.append(_load_image(obj_path))
            return all_returns

        return wrapper

    return decorator
