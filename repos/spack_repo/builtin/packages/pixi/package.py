# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.bundle import BundlePackage

from spack.package import *

class Pixi(BundlePackage):
    """Pixi is a fast, modern, and reproducible package management tool for
    developers of all backgrounds."""

    homepage = "https://pixi.sh/latest/"

    maintainers = ['vanderwb']
    
    version('1.0.0')
