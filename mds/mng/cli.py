#!/usr/bin/env python

"""
CLI Interface for mds-toolbox.
"""

__author__ = "Antonio Mariani"
__email__ = "antonio.mariani@cmcc.it"

import click

from mds import mds_s3
from mds import wrapper


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-o", "--output-directory", required=True, type=str, help="Output directory"
)
@click.option(
    "-f", "--output-filename", required=True, type=str, help="Output filename"
)
@click.option("-i", "--dataset-id", required=True, type=str, help="Dataset Id")
@click.option(
    "-v", "--variables", multiple=True, type=str, help="Variables to download"
)
@click.option(
    "-x", "--minimum-longitude", type=float, help="Minimum longitude for the subset."
)
@click.option(
    "-X", "--maximum-longitude", type=float, help="Maximum longitude for the subset. "
)
@click.option(
    "-y",
    "--minimum-latitude",
    type=float,
    help="Minimum latitude for the subset. Requires a float within this range:  [-90<=x<=90]",
)
@click.option(
    "-Y",
    "--maximum-latitude",
    type=float,
    help="Maximum latitude for the subset. Requires a float within this range:  [-90<=x<=90]",
)
@click.option(
    "-z",
    "--minimum-depth",
    type=float,
    help="Minimum depth for the subset. Requires a float within this range:  [x>=0]",
)
@click.option(
    "-Z",
    "--maximum-depth",
    type=float,
    help="Maximum depth for the subset. Requires a float within this range:  [x>=0]",
)
@click.option(
    "-t",
    "--start-datetime",
    type=str,
    default=False,
    help="Start datetime as: %Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S|%Y-%m-%dT%H:%M:%S.%fZ",
)
@click.option(
    "-T",
    "--end-datetime",
    type=str,
    default=False,
    help="End datetime as: %Y|%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S|%Y-%m-%dT%H:%M:%S.%fZ",
)
@click.option("-r", "--dry-run", is_flag=True, default=False, help="Dry run")
@click.option(
    "-g", "--dataset-version", type=str, default=None, help="Dataset version or tag"
)
@click.option("-n", "--username", type=str, default=None, help="Username")
@click.option("-w", "--password", type=str, default=None, help="Password")
def subset(**kwargs):
    wrapper.mds_download("subset", **kwargs)


@cli.command()
@click.option(
    "-f", "--filter", required=False, type=str, help="Filter on the online files"
)
@click.option(
    "-o", "--output-directory", required=True, type=str, help="Output directory"
)
@click.option("-i", "--dataset-id", required=True, type=str, help="Dataset Id")
@click.option(
    "-g", "--dataset-version", type=str, default=None, help="Dataset version or tag"
)
# @click.option('-s', '--service', type=str, default='files',
#               help="Force download through one of the available services using the service name among "
#                    "['original-files', 'ftp'] or its short name among ['files', 'ftp'].")
@click.option("-d", "--dry-run", is_flag=True, default=False, help="Dry run")
@click.option(
    "-u",
    "--update",
    is_flag=True,
    default=False,
    help="If the file not exists, download it, otherwise update it it changed on mds",
)
@click.option("-v", "--dataset-version", type=str, default=None, help="Dry run")
@click.option(
    "-nd",
    "--no-directories",
    type=str,
    default=True,
    help="Option to not recreate folder hierarchy in output directory",
)
@click.option(
    "--force-download",
    type=str,
    default=True,
    help="Flag to skip confirmation before download",
)
@click.option(
    "--disable-progress-bar", type=str, default=True, help="Flag to hide progress bar"
)
@click.option("-n", "--username", type=str, default=None, help="Username")
@click.option("-w", "--password", type=str, default=None, help="Password")
def get(**kwargs):
    update = kwargs.pop("update")
    if update:
        wrapper.mds_update_download(**kwargs)
    else:
        wrapper.mds_download("get", **kwargs)


@cli.command()
@click.argument("dataset_id", type=str)
@click.argument("mds_filter", type=str)
@click.option(
    "-g", "--dataset-version", type=str, default=None, help="Dataset version or tag"
)
def file_list(*args, **kwargs):
    mds_file_list = wrapper.mds_list(*args, **kwargs)
    print(f"{' '.join(mds_file_list)}")


@cli.command()
@click.option(
    "-e",
    "--s3_file",
    type=str,
    default=None,
    help="Path to a specific s3 file - if present, other parameters are ignored.",
)
@click.option("-p", "--product", type=str, default=None, help="The product name")
@click.option("-i", "--dataset_id", type=str, default=None, help="The datasetID")
@click.option(
    "-g",
    "--version",
    type=str,
    default=None,
    help="Force the selection of a specific dataset version",
)
@click.option(
    "-s",
    "--subdir",
    type=str,
    default=None,
    help="Subdir structure on mds (i.e. {year}/{month})",
)
@click.option(
    "-f",
    "--mds_filter",
    type=str,
    default=None,
    help="Pattern to filter data (no regex)",
)
def etag(**kwargs):
    s3_files = wrapper.mds_etag(**kwargs)
    for s3_file in s3_files:
        print(f"{s3_file.name} {s3_file.etag}")


@cli.command()
@click.option(
    "-b", "--bucket", "s3_bucket", required=True, type=str, help="Bucket name"
)
@click.option(
    "-f",
    "--filter",
    "file_filter",
    required=True,
    type=str,
    help="Filter on the online files",
)
@click.option(
    "-o", "--output-directory", required=True, type=str, help="Output directory"
)
@click.option("-p", "--product", required=True, type=str, help="The product name")
@click.option("-i", "--dataset-id", required=True, type=str, help="Dataset Id")
@click.option(
    "-g", "--dataset-version", type=str, default=None, help="Dataset version or tag"
)
@click.option(
    "-r", "--recursive", is_flag=True, default=False, help="List recursive all s3 files"
)
@click.option(
    "--threads",
    "n_threads",
    type=int,
    default=None,
    help="Downloading file using threads",
)
@click.option(
    "-s",
    "--subdir",
    type=str,
    default=None,
    help="Dataset directory on mds (i.e. {year}/{month}) - If present boost the connection",
)
@click.option(
    "--overwrite",
    required=False,
    is_flag=True,
    default=False,
    help="Force overwrite of the file",
)
@click.option(
    "--keep-timestamps",
    required=False,
    is_flag=True,
    default=False,
    help="After the download, set the correct timestamp to the file",
)
@click.option(
    "--sync-time",
    required=False,
    is_flag=True,
    default=False,
    help="Update the file if it changes on the server using last update information",
)
@click.option(
    "--sync-etag",
    required=False,
    is_flag=True,
    default=False,
    help="Update the file if it changes on the server using etag information",
)
def s3_get(**kwargs):
    mds_s3.download_files(**kwargs)


@cli.command()
@click.option(
    "-b",
    "--bucket",
    "s3_bucket",
    required=True,
    type=str,
    help="Filter on the online files",
)
@click.option(
    "-f",
    "--filter",
    "file_filter",
    required=True,
    type=str,
    help="Filter on the online files",
)
@click.option("-p", "--product", required=True, type=str, help="The product name")
@click.option("-i", "--dataset-id", required=False, type=str, help="Dataset Id")
@click.option(
    "-g", "--dataset-version", type=str, default=None, help="Dataset version or tag"
)
@click.option(
    "-s",
    "--subdir",
    type=str,
    default=None,
    help="Dataset directory on mds (i.e. {year}/{month}) - If present boost the connection",
)
@click.option(
    "-r", "--recursive", is_flag=True, default=False, help="List recursive all s3 files"
)
def s3_list(**kwargs):
    s3_files = mds_s3.get_file_list(**kwargs)
    print(f"{' '.join([f.file for f in s3_files])}")


if __name__ == "__main__":
    cli()
