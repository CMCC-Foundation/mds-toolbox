import fnmatch
import os
import pytest

import mds.core.wrapper
from mds.core import utils


def test_get_temporary_directory():
    output_filename = "test.nc"
    destination_dir = "/my_dir"
    result = utils.get_temporary_directory(output_filename, destination_dir)
    result2 = utils.get_temporary_directory(output_filename, destination_dir)

    assert result == f"{destination_dir}/.c69843c60260734a065df6f9bcaca942"
    assert result == result2


def test_cwf():
    home = os.environ["HOME"]
    os.chdir(home)

    os.chdir(home)
    cwd = utils.cwd()

    assert cwd == home


def test_mds_download_wrong_mode(tmp_path):
    with pytest.raises(ValueError):
        mds.download.wrapper.mds_download("wrong")


def test_mds_get_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        dataset = "cmems_mod_med_phy-tem_anfc_4.2km_P1D-m"
        output_filename = (
            "20231231_d-CMCC--TEMP-MFSeas8-MEDATL-b2024gsagaga109_an-sv09.00.nc"
        )
        output_path = f"{tmp_path}"

        mds.download.wrapper.mds_download(
            "get",
            filter=output_filename,
            output_directory=output_path,
            dataset_id=dataset,
        )


def test_mds_get_download(tmp_path):
    dataset = "cmems_mod_med_phy-tem_anfc_4.2km_P1D-m"
    output_filename = "20231231_d-CMCC--TEMP-MFSeas8-MEDATL-b20240109_an-sv09.00.nc"
    output_path = f"{tmp_path}"

    mds.download.wrapper.mds_download(
        "get", filter=output_filename, output_directory=output_path, dataset_id=dataset
    )

    assert os.path.exists(os.path.join(output_path, output_filename))


def test_mds_get_list():
    dataset = "cmems_mod_med_phy-tem_anfc_4.2km_P1D-m"
    mds_filter = "*-CMCC--TEMP-MFSeas8-MEDATL-b20240109_an-sv09.00.nc"

    result = mds.download.wrapper.mds_list(dataset, mds_filter)

    assert isinstance(result, list)
    # best analysis keep on mds
    assert len(result) == 7


def test_fnmatch():
    s3_file = "_2.5km_PT1H-m_202311/2023/12/20231201_h-CMCC--TEMP-BSeas6-BS-b20231212_an-sv12.00.nc"

    assert fnmatch.fnmatch(s3_file, "*20231201_h-CMCC*")
    assert not fnmatch.fnmatch(s3_file, "*20231201_h-cmcc*")
    assert not fnmatch.fnmatch(s3_file, "*2023201_h*")
