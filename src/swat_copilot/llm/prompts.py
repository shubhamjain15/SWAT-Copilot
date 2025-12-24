"""Prompt templates for LLM interactions."""

from typing import Any


class PromptTemplates:
    """Prompt templates for SWAT-related LLM queries."""

    @staticmethod
    def project_summary_prompt(project_info: dict[str, Any]) -> str:
        """
        Generate prompt for project summary.

        Args:
            project_info: Project information dictionary

        Returns:
            Formatted prompt
        """
        return f"""
You are analyzing a SWAT (Soil and Water Assessment Tool) model project.

Project Information:
- Name: {project_info.get('name', 'Unknown')}
- Path: {project_info.get('path', 'Unknown')}
- Has Outputs: {project_info.get('has_outputs', False)}
- Total Files: {project_info.get('file_count', 0)}

Please provide a comprehensive summary of this SWAT project, including:
1. Project structure and organization
2. Available input files and their purpose
3. Output files (if available) and what they contain
4. Any notable characteristics or configurations

Format your response in a clear, structured manner suitable for a hydrologist or environmental modeler.
"""

    @staticmethod
    def variable_explanation_prompt(variable_name: str, output_type: str) -> str:
        """
        Generate prompt for variable explanation.

        Args:
            variable_name: Name of the variable
            output_type: Type of output (reach, subbasin, hru)

        Returns:
            Formatted prompt
        """
        return f"""
Explain the SWAT model variable '{variable_name}' from the {output_type} output file.

Please include:
1. Full name and definition
2. Units of measurement
3. Physical meaning and interpretation
4. Typical range of values
5. How it's used in hydrological analysis

Provide a clear, concise explanation suitable for both technical and non-technical users.
"""

    @staticmethod
    def analysis_recommendation_prompt(
        project_summary: dict[str, Any],
        user_goal: str,
    ) -> str:
        """
        Generate prompt for analysis recommendations.

        Args:
            project_summary: Project summary data
            user_goal: User's analysis goal

        Returns:
            Formatted prompt
        """
        return f"""
A user is working with a SWAT model project and wants to: {user_goal}

Project Summary:
{project_summary}

As an expert in SWAT modeling and hydrological analysis, recommend:
1. Which output variables to analyze
2. What statistical methods to apply
3. How to interpret the results
4. Any visualizations that would be helpful
5. Potential limitations or considerations

Provide practical, actionable recommendations.
"""

    @staticmethod
    def water_balance_interpretation_prompt(balance_data: dict[str, float]) -> str:
        """
        Generate prompt for water balance interpretation.

        Args:
            balance_data: Water balance components

        Returns:
            Formatted prompt
        """
        components = "\n".join([f"- {k}: {v:.2f} mm" for k, v in balance_data.items()])

        return f"""
Analyze the following water balance components from a SWAT model simulation:

{components}

Please provide:
1. Overall water balance assessment
2. Dominant hydrological processes
3. Any anomalies or concerns
4. Implications for watershed management
5. Recommendations for model validation or calibration

Focus on practical interpretation for watershed modeling applications.
"""

    @staticmethod
    def calibration_guidance_prompt(
        variable: str,
        observed_stats: dict[str, float],
        simulated_stats: dict[str, float],
    ) -> str:
        """
        Generate prompt for calibration guidance.

        Args:
            variable: Variable being calibrated
            observed_stats: Observed data statistics
            simulated_stats: Simulated data statistics

        Returns:
            Formatted prompt
        """
        return f"""
You are assisting with SWAT model calibration for the variable: {variable}

Observed Statistics:
{observed_stats}

Simulated Statistics:
{simulated_stats}

Provide calibration guidance including:
1. Assessment of model performance
2. Which SWAT parameters are most sensitive for this variable
3. Recommended parameter adjustment direction (increase/decrease)
4. Expected impact of parameter changes
5. Calibration strategy and priorities

Base your recommendations on established SWAT calibration procedures and hydrological principles.
"""

    @staticmethod
    def query_output_prompt(query: str, available_variables: list[str]) -> str:
        """
        Generate prompt for interpreting user queries about outputs.

        Args:
            query: User's question
            available_variables: List of available variables

        Returns:
            Formatted prompt
        """
        vars_list = ", ".join(available_variables[:20])
        if len(available_variables) > 20:
            vars_list += "..."

        return f"""
User Question: {query}

Available SWAT Output Variables:
{vars_list}

Based on the user's question and available variables:
1. Identify which variables are relevant to answer the question
2. Suggest appropriate analysis methods
3. Recommend visualizations
4. Provide context about what the analysis will reveal

Be specific about variable names and analysis techniques.
"""
