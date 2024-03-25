"""Module containing custom types
"""

from typing import Annotated, Literal, TypeVar

import numpy as np
import numpy.typing as npt


DType = TypeVar("DType", bound=np.generic)

NDArray3 = Annotated[npt.NDArray[DType], Literal[3]]

NDArray3xNxN = Annotated[npt.NDArray[DType], Literal[3, "N", "N"]]
