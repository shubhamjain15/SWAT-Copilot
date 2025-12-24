"""MCP Server implementation for SWAT model interaction."""

import logging
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

from swat_copilot.config.settings import get_settings
from swat_copilot.core.projects import SWATProject
from swat_copilot.services.project_manager import ProjectManager
from swat_copilot.services.summary import SummarizeService
from swat_copilot.services.analysis import AnalysisService
from swat_copilot.visualization.plots import SWATPlotter

logger = logging.getLogger(__name__)


class SWATMCPServer:
    """
    MCP Server for SWAT model interaction.

    Provides tools and resources for AI assistants to:
    - Locate and load SWAT projects
    - Read and summarize inputs/outputs
    - Perform analysis and calculations
    - Generate visualizations
    """

    def __init__(self) -> None:
        """Initialize SWAT MCP Server."""
        self.settings = get_settings()
        self.server = Server(self.settings.mcp_server_name)
        self.project_manager = ProjectManager()
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Setup MCP protocol handlers."""

        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            """List available SWAT project resources."""
            resources = []

            # If a project is loaded, expose it as a resource
            if self.project_manager.current_project:
                project = self.project_manager.current_project
                resources.append(
                    Resource(
                        uri=AnyUrl(f"swat://project/{project.name}"),
                        name=f"SWAT Project: {project.name}",
                        mimeType="application/json",
                        description=f"SWAT project at {project.project_path}",
                    )
                )

                # Add output files as resources
                for output_file in project.output_files:
                    resources.append(
                        Resource(
                            uri=AnyUrl(f"swat://output/{output_file.file_type.value}"),
                            name=f"Output: {output_file.name}",
                            mimeType="text/plain",
                            description=f"{output_file.file_type.value} output file",
                        )
                    )

            return resources

        @self.server.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            """Read a SWAT project resource."""
            uri_str = str(uri)

            if uri_str.startswith("swat://project/"):
                return await self._read_project_resource()
            elif uri_str.startswith("swat://output/"):
                output_type = uri_str.split("/")[-1]
                return await self._read_output_resource(output_type)

            raise ValueError(f"Unknown resource URI: {uri}")

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available SWAT analysis tools."""
            return [
                Tool(
                    name="find_swat_projects",
                    description="Find SWAT projects in a directory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "search_path": {
                                "type": "string",
                                "description": "Directory path to search for SWAT projects",
                            },
                            "max_depth": {
                                "type": "integer",
                                "description": "Maximum search depth (default: 3)",
                                "default": 3,
                            },
                        },
                    },
                ),
                Tool(
                    name="load_swat_project",
                    description="Load a SWAT project from a directory path",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to SWAT project directory",
                            },
                        },
                        "required": ["project_path"],
                    },
                ),
                Tool(
                    name="get_project_summary",
                    description="Get comprehensive summary of loaded SWAT project",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="get_output_summary",
                    description="Get summary of SWAT model outputs",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="get_variable_statistics",
                    description="Calculate statistics for a SWAT output variable",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "variable": {
                                "type": "string",
                                "description": "Variable name (e.g., 'FLOW_OUT', 'SED_OUT')",
                            },
                            "output_type": {
                                "type": "string",
                                "enum": ["reach", "subbasin", "hru"],
                                "description": "Type of output file",
                                "default": "reach",
                            },
                            "spatial_id": {
                                "type": "integer",
                                "description": "Optional reach/subbasin/HRU ID to filter",
                            },
                        },
                        "required": ["variable"],
                    },
                ),
                Tool(
                    name="get_time_series",
                    description="Get time series data for a variable",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "variable": {
                                "type": "string",
                                "description": "Variable name",
                            },
                            "output_type": {
                                "type": "string",
                                "enum": ["reach", "subbasin", "hru"],
                                "default": "reach",
                            },
                            "spatial_id": {
                                "type": "integer",
                                "description": "Optional spatial unit ID",
                            },
                        },
                        "required": ["variable"],
                    },
                ),
                Tool(
                    name="calculate_water_balance",
                    description="Calculate water balance components from outputs",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "output_type": {
                                "type": "string",
                                "enum": ["reach", "subbasin", "hru"],
                                "default": "subbasin",
                            },
                        },
                    },
                ),
                Tool(
                    name="plot_time_series",
                    description="Generate time series plot for a variable",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "variable": {
                                "type": "string",
                                "description": "Variable name to plot",
                            },
                            "output_type": {
                                "type": "string",
                                "enum": ["reach", "subbasin", "hru"],
                                "default": "reach",
                            },
                            "spatial_id": {
                                "type": "integer",
                                "description": "Optional spatial unit ID",
                            },
                            "title": {
                                "type": "string",
                                "description": "Plot title",
                            },
                        },
                        "required": ["variable"],
                    },
                ),
                Tool(
                    name="plot_comparison",
                    description="Create comparison plot for multiple variables",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "variables": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of variables to compare",
                            },
                            "output_type": {
                                "type": "string",
                                "enum": ["reach", "subbasin", "hru"],
                                "default": "reach",
                            },
                        },
                        "required": ["variables"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent | ImageContent | EmbeddedResource]:
            """Execute a SWAT analysis tool."""
            logger.info(f"Executing tool: {name} with arguments: {arguments}")

            try:
                if name == "find_swat_projects":
                    return await self._find_projects(arguments)
                elif name == "load_swat_project":
                    return await self._load_project(arguments)
                elif name == "get_project_summary":
                    return await self._get_project_summary()
                elif name == "get_output_summary":
                    return await self._get_output_summary()
                elif name == "get_variable_statistics":
                    return await self._get_variable_statistics(arguments)
                elif name == "get_time_series":
                    return await self._get_time_series(arguments)
                elif name == "calculate_water_balance":
                    return await self._calculate_water_balance(arguments)
                elif name == "plot_time_series":
                    return await self._plot_time_series(arguments)
                elif name == "plot_comparison":
                    return await self._plot_comparison(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

            except Exception as e:
                logger.error(f"Error executing tool {name}: {e}", exc_info=True)
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    async def _find_projects(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Find SWAT projects in a directory."""
        search_path = Path(arguments.get("search_path", "."))
        max_depth = arguments.get("max_depth", 3)

        projects = self.project_manager.find_projects(search_path, max_depth)

        result = {
            "search_path": str(search_path),
            "max_depth": max_depth,
            "projects_found": len(projects),
            "projects": [str(p) for p in projects],
        }

        return [TextContent(type="text", text=str(result))]

    async def _load_project(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Load a SWAT project."""
        project_path = Path(arguments["project_path"])
        project = self.project_manager.load_project(project_path)

        result = {
            "success": True,
            "project_name": project.name,
            "project_path": str(project.project_path),
            "file_count": sum(len(files) for files in project.files.values()),
            "has_outputs": project.has_outputs(),
        }

        return [TextContent(type="text", text=str(result))]

    async def _get_project_summary(self) -> list[TextContent]:
        """Get project summary."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        service = SummarizeService(self.project_manager.current_project)
        summary = service.get_project_summary()

        return [TextContent(type="text", text=str(summary))]

    async def _get_output_summary(self) -> list[TextContent]:
        """Get output summary."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        service = SummarizeService(self.project_manager.current_project)
        summary = service.get_output_summary()

        return [TextContent(type="text", text=str(summary))]

    async def _get_variable_statistics(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Get variable statistics."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        service = AnalysisService(self.project_manager.current_project)
        stats = service.get_variable_statistics(
            variable=arguments["variable"],
            output_type=arguments.get("output_type", "reach"),
            spatial_id=arguments.get("spatial_id"),
        )

        return [TextContent(type="text", text=str(stats))]

    async def _get_time_series(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Get time series data."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        service = AnalysisService(self.project_manager.current_project)
        data = service.get_time_series(
            variable=arguments["variable"],
            output_type=arguments.get("output_type", "reach"),
            spatial_id=arguments.get("spatial_id"),
        )

        if data is None:
            return [TextContent(type="text", text="No data found for specified variable")]

        return [TextContent(type="text", text=data.to_string())]

    async def _calculate_water_balance(self, arguments: dict[str, Any]) -> list[TextContent]:
        """Calculate water balance."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        service = AnalysisService(self.project_manager.current_project)
        balance = service.calculate_water_balance(
            output_type=arguments.get("output_type", "subbasin")
        )

        return [TextContent(type="text", text=str(balance))]

    async def _plot_time_series(self, arguments: dict[str, Any]) -> list[ImageContent]:
        """Generate time series plot."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        plotter = SWATPlotter(self.project_manager.current_project)
        image_data = plotter.plot_time_series(
            variable=arguments["variable"],
            output_type=arguments.get("output_type", "reach"),
            spatial_id=arguments.get("spatial_id"),
            title=arguments.get("title"),
        )

        return [ImageContent(type="image", data=image_data, mimeType="image/png")]

    async def _plot_comparison(self, arguments: dict[str, Any]) -> list[ImageContent]:
        """Generate comparison plot."""
        if not self.project_manager.current_project:
            raise ValueError("No project loaded. Use 'load_swat_project' first.")

        plotter = SWATPlotter(self.project_manager.current_project)
        image_data = plotter.plot_comparison(
            variables=arguments["variables"],
            output_type=arguments.get("output_type", "reach"),
        )

        return [ImageContent(type="image", data=image_data, mimeType="image/png")]

    async def _read_project_resource(self) -> str:
        """Read project resource."""
        if not self.project_manager.current_project:
            return "No project loaded"

        service = SummarizeService(self.project_manager.current_project)
        return str(service.get_project_summary())

    async def _read_output_resource(self, output_type: str) -> str:
        """Read output resource."""
        if not self.project_manager.current_project:
            return "No project loaded"

        service = SummarizeService(self.project_manager.current_project)
        summary = service.get_output_summary()

        # Find specific output type in summary
        for output in summary.get("output_files", []):
            if output.get("type") == output_type:
                return str(output)

        return f"Output type {output_type} not found"

    async def run(self) -> None:
        """Run the MCP server."""
        logger.info(f"Starting {self.settings.mcp_server_name} v{self.settings.mcp_server_version}")

        # Run server based on transport type
        if self.settings.mcp_transport == "stdio":
            from mcp.server.stdio import stdio_server

            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options(),
                )
        else:
            raise ValueError(f"Unsupported transport: {self.settings.mcp_transport}")
