#!/usr/bin/env python
import sys

from setuptools import find_namespace_packages, setup

if sys.version_info < (3, 7):
    print("Error: Soda SQL requires at least Python 3.7")
    print("Error: Please upgrade your Python version to 3.7 or later")
    sys.exit(1)

package_name = "soda-core-snowflake"
package_version = "3.0.11"
description = "Soda Core Snowflake Package"

requires = [
    f"soda-core=={package_version}",
    "snowflake-connector-python~=2.7",
    # https://github.com/snowflakedb/snowflake-connector-python/issues/1206
    "typing-extensions>=4.3.0",
    "pyarrow<8.1.0,>=8.0.0",
]
# TODO Fix the params
setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["soda*"]),
)
