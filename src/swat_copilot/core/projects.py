"""Domain models that understand the layout and semantics of SWAT projects."""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class SWATFileType(Enum):
    """Types of SWAT model files."""

    # Input files
    MASTER_WATERSHED = "master_watershed"  # .Master.Watershed.dat
    CONTROL = "control"  # file.cio
    SUBBASIN = "subbasin"  # .sub
    HRU = "hru"  # .hru
    ROUTING = "routing"  # .rte
    WEATHER = "weather"  # .pcp, .tmp, .slr, .hmd, .wnd
    SOIL = "soil"  # .sol
    MANAGEMENT = "management"  # .mgt
    GROUNDWATER = "groundwater"  # .gw
    RESERVOIR = "reservoir"  # .res
    POND = "pond"  # .pnd

    # Output files
    OUTPUT_STD = "output_std"  # output.std
    OUTPUT_RCH = "output_rch"  # output.rch
    OUTPUT_SUB = "output_sub"  # output.sub
    OUTPUT_HRU = "output_hru"  # output.hru
    OUTPUT_RSV = "output_rsv"  # output.rsv

    # Configuration
    CONFIG = "config"
    UNKNOWN = "unknown"


@dataclass
class SWATFile:
    """Represents a single SWAT model file."""

    path: Path
    file_type: SWATFileType
    description: str = ""

    @property
    def exists(self) -> bool:
        """Check if the file exists."""
        return self.path.exists()

    @property
    def size(self) -> int:
        """Get file size in bytes."""
        return self.path.stat().st_size if self.exists else 0

    @property
    def name(self) -> str:
        """Get file name."""
        return self.path.name


@dataclass
class SWATProject:
    """Represents a complete SWAT model project."""

    project_path: Path
    name: str
    description: str = ""
    files: dict[SWATFileType, list[SWATFile]] = field(default_factory=dict)
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate project path exists."""
        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {self.project_path}")

    @property
    def input_files(self) -> list[SWATFile]:
        """Get all input files."""
        input_types = [
            SWATFileType.MASTER_WATERSHED,
            SWATFileType.CONTROL,
            SWATFileType.SUBBASIN,
            SWATFileType.HRU,
            SWATFileType.ROUTING,
            SWATFileType.WEATHER,
            SWATFileType.SOIL,
            SWATFileType.MANAGEMENT,
            SWATFileType.GROUNDWATER,
            SWATFileType.RESERVOIR,
            SWATFileType.POND,
        ]
        return [f for ft in input_types for f in self.files.get(ft, [])]

    @property
    def output_files(self) -> list[SWATFile]:
        """Get all output files."""
        output_types = [
            SWATFileType.OUTPUT_STD,
            SWATFileType.OUTPUT_RCH,
            SWATFileType.OUTPUT_SUB,
            SWATFileType.OUTPUT_HRU,
            SWATFileType.OUTPUT_RSV,
        ]
        return [f for ft in output_types for f in self.files.get(ft, [])]

    def get_file(self, file_type: SWATFileType, index: int = 0) -> Optional[SWATFile]:
        """Get a specific file by type and index."""
        files = self.files.get(file_type, [])
        return files[index] if index < len(files) else None

    def has_outputs(self) -> bool:
        """Check if project has output files."""
        return len(self.output_files) > 0


class SWATProjectLocator:
    """Locate and identify SWAT projects in a directory structure."""

    @staticmethod
    def is_swat_project(path: Path) -> bool:
        """Check if a directory contains a SWAT project."""
        if not path.is_dir():
            return False

        # Look for characteristic SWAT files
        indicators = [
            "file.cio",  # Control file
            "*.Master.Watershed.dat",
        ]

        for indicator in indicators:
            if list(path.glob(indicator)):
                return True

        return False

    @staticmethod
    def find_swat_projects(root_path: Path, max_depth: int = 3) -> list[Path]:
        """
        Find all SWAT projects under a root directory.

        Args:
            root_path: Root directory to search
            max_depth: Maximum depth to search

        Returns:
            List of paths containing SWAT projects
        """
        projects = []

        def search(current_path: Path, depth: int) -> None:
            if depth > max_depth:
                return

            if SWATProjectLocator.is_swat_project(current_path):
                projects.append(current_path)
                return  # Don't search subdirectories of a project

            if current_path.is_dir():
                for child in current_path.iterdir():
                    if child.is_dir():
                        search(child, depth + 1)

        search(root_path, 0)
        return projects

    @staticmethod
    def scan_project_files(project_path: Path) -> dict[SWATFileType, list[SWATFile]]:
        """
        Scan a SWAT project directory and categorize all files.

        Args:
            project_path: Path to SWAT project

        Returns:
            Dictionary mapping file types to lists of SWATFile objects
        """
        files: dict[SWATFileType, list[SWATFile]] = {}

        if not project_path.is_dir():
            return files

        # Define file patterns for each type
        patterns = {
            SWATFileType.CONTROL: ["file.cio"],
            SWATFileType.MASTER_WATERSHED: ["*.Master.Watershed.dat"],
            SWATFileType.SUBBASIN: ["*.sub"],
            SWATFileType.HRU: ["*.hru"],
            SWATFileType.ROUTING: ["*.rte"],
            SWATFileType.SOIL: ["*.sol"],
            SWATFileType.MANAGEMENT: ["*.mgt"],
            SWATFileType.GROUNDWATER: ["*.gw"],
            SWATFileType.RESERVOIR: ["*.res"],
            SWATFileType.POND: ["*.pnd"],
            SWATFileType.WEATHER: ["*.pcp", "*.tmp", "*.slr", "*.hmd", "*.wnd"],
            SWATFileType.OUTPUT_STD: ["output.std"],
            SWATFileType.OUTPUT_RCH: ["output.rch"],
            SWATFileType.OUTPUT_SUB: ["output.sub"],
            SWATFileType.OUTPUT_HRU: ["output.hru"],
            SWATFileType.OUTPUT_RSV: ["output.rsv"],
        }

        for file_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                for file_path in project_path.glob(pattern):
                    if file_path.is_file():
                        swat_file = SWATFile(
                            path=file_path,
                            file_type=file_type,
                        )
                        files.setdefault(file_type, []).append(swat_file)

        return files
