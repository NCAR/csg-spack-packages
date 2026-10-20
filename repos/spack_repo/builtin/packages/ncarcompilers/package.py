# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *
import os

class Ncarcompilers(MakefilePackage):
    """ncarcompilers provides a wrapper that sits in front of compiler binaries
    and MPI wrappers in the users PATH. The wrapper inserts header and library
    flags to each build command based on settings inserted into environment
    modules."""

    homepage = "https://github.com/NCAR/ncarcompilers"
    git      = "https://github.com/NCAR/ncarcompilers.git"
    url      = "https://github.com/NCAR/ncarcompilers/archive/refs/tags/v0.7.1.tar.gz"

    maintainers = ['vanderwb']

    version('main',  branch='main')
    version('1.2.0', sha256='6b371891a39642115b38b0a05c688575e9c5c56f5393eff1c3d200cfaa74d4aa')
    version('1.1.0', sha256='ebfb6b635c1270e318d3cda688a2f2971cd5ac1aed963a7556fe9214c08201bb')
    version('1.0.0', sha256='99e08722cbfd7aeeb7dfaec18ae9753f9beeeeddfd37b9dc1b0ea7ed40b249d9')
    version('0.8.0', sha256='f9049ee4d63f52c3c971604b72e41d27a913e87b968b5c7f2cbcb08871affed9')
    version('0.7.2', sha256='f0a1b7a8bd271e2ec41eebdbb2bf2d0ae91f8e197dba06a9c7b67f671f41e819')
    version('0.7.1', sha256='88f23f89841b6e49a44b66d3a6afb3d8d817f51103cc07f3c8c48864a0215405')

    variant("mpi", default = True, description = "Install MPI wrappers")
    variant("hip", default = False, description = "Install wrappers for HIP LLVM")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    conflicts("+hip", "@:1.0.0")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        # The real compilers need to be in the PATH, because Spack wrappers don't always map
        # I.e. ifort is missing for oneapi
        env.append_path("PATH", ancestor(self.compiler.cc))

        # Make sure traditional intel compilers are in the path too
        with when("%oneapi@:2024"):
            env.append_path("PATH", join_path(ancestor(self.compiler.cc), "intel64"))

    def build(self, spec, prefix):
        make()

        if spec.satisfies("+mpi"):
            make("mpi")
        if spec.satisfies("+hip"):
            make("hip")

    def install(self, spec, prefix):
        make('install', 'PREFIX={}'.format(prefix))

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        """Adds environment variables to the generated module file.
        from setting CC/CXX/F77/FC
        """

        env.set("CC", os.path.basename(self.compiler.cc))
        env.set("CXX", os.path.basename(self.compiler.cxx))
        env.set("F77", os.path.basename(self.compiler.f77))
        env.set("FC", os.path.basename(self.compiler.fc))

        if self.spec.satisfies("+mpi"):
            env.set("NCAR_WRAPPER_MPI_PATH", join_path(self.prefix.bin, "mpi"))
        if self.spec.satisfies("+hip"):
            env.set("NCAR_WRAPPER_HIP_PATH",  join_path(self.prefix.bin, "hip"))
            env.set("NCAR_WRAPPER_HIP_CLANG", join_path(self.prefix.bin, "llvm-amd"))
