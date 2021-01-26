# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Application entry point."""
from pathlib import Path

from kedro.context import KedroContext, load_context
from kedro.extras.transformers import ProfileTimeTransformer  # new import
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog

from .memory_profile import ProfileMemoryTransformer  # new import


class TransformerHooks:
    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog) -> None:
        catalog.add_transformer(ProfileTimeTransformer())
        catalog.add_transformer(ProfileMemoryTransformer(), "master_table")


class ProjectContext(KedroContext):
    """Users can override the remaining methods from the parent class here,
    or create new ones (e.g. as required by plugins)
    """

    hooks = (
        # register the collection of your Hook implementations here.
        # Note that we are using an instance here, not a class. It could also be a
        # module.
        TransformerHooks(),
    )
    # You can add more than one hook by simply listing them
    # in a tuple.`hooks = (Hook1(), Hook2())`


def run_package():
    # entry point for running pip-install projects
    # using `<project_package>` command
    project_context = load_context(Path.cwd())
    project_context.run()


if __name__ == "__main__":
    # entry point for running pip-installed projects
    # using `python -m <project_package>.run` command
    run_package()
