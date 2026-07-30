"""
===============================================================================
AI-Powered E-Commerce Analytics & Sales Forecasting Platform
===============================================================================
File: utils.py
Description: Helper utility functions for data formatting, statistical calculations,
             export operations, report generation, and reusable UI components.

Author: Senior Data Scientist & UI/UX Engineer
Date: July 2026
===============================================================================
"""

import io
import logging
from typing import Dict, Any, Tuple, Optional, List
import pandas as pd
import numpy as np
import streamlit as st

# Setup logger for utility operations
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# =============================================================================
# 1. CURRENCY & NUMBER FORMATTING
# =============================================================================
def format_currency(value: float, currency_symbol: str = "$") -> str:
    """
    Formats a numeric value as currency with appropriate thousand separators
    and dynamic abbreviations (K, M, B) for clean KPI card display.
    
    Args:
        value (float): The numerical value to format.
        currency_symbol (str): Symbol to prefix (e.g., '$', '₹', '€').
        
    Returns:
        str: Formatted currency string.
    """
    try:
        if pd.isna(value) or value is None:
            return f"{currency_symbol}0.00"
        
        abs_val = abs(value)
        sign = "-" if value < 0 else ""

        if abs_val >= 1_000_000_000:
            return f"{sign}{currency_symbol}{abs_val / 1_000_000_000:.2f}B"
        elif abs_val >= 1_000_000:
            return f"{sign}{currency_symbol}{abs_val / 1_000_000:.2f}M"
        elif abs_val >= 1_000:
            return f"{sign}{currency_symbol}{abs_val / 1_000:.2f}K"
        else:
            return f"{sign}{currency_symbol}{abs_val:,.2f}"
    except Exception as e:
        logger.error(f"Error formatting currency value {value}: {str(e)}")
        return f"{currency_symbol}{value}"


def format_number(value: float, decimal_places: int = 2) -> str:
    """
    Formats general numbers with dynamic suffixes (K, M, B) or standard decimal places.
    
    Args:
        value (float): Number to format.
        decimal_places (int): Number of decimals if small value.
        
    Returns:
        str: Formatted string representation.
    """
    try:
        if pd.isna(value) or value is None:
            return "0"
        
        abs_val = abs(value)
        sign = "-" if value < 0 else ""

        if abs_val >= 1_000_000_000:
            return f"{sign}{abs_val / 1_000_000_000:.2f}B"
        elif abs_val >= 1_000_000:
            return f"{sign}{abs_val / 1_000_000:.2f}M"
        elif abs_val >= 1_000:
            return f"{sign}{abs_val / 1_000:.2f}K"
        else:
            return f"{sign}{abs_val:,.{decimal_places}f}"
    except Exception as e:
        logger.error(f"Error formatting number {value}: {str(e)}")
        return str(value)


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """
    Formats decimal values as percentages.
    
    Args:
        value (float): Numerical percentage value (e.g., 15.5 or 0.155).
        decimal_places (int): Decimal precision.
        
    Returns:
        str: Formatted percentage string.
    """
    try:
        if pd.isna(value) or value is None:
            return "0.00%"
        return f"{value:.{decimal_places}f}%"
    except Exception as e:
        logger.error(f"Error formatting percentage {value}: {str(e)}")
        return f"{value}%"


# =============================================================================
# 2. DATA PROCESSING & STATISTICAL HELPERS
# =============================================================================
def calculate_data_health_score(df: pd.DataFrame) -> Tuple[int, Dict[str, Any]]:
    """
    Calculates an overall data health score (0-100%) based on missing values,
    duplicates, and data type correctness.
    
    Args:
        df (pd.DataFrame): Input dataframe.
        
    Returns:
        Tuple[int, Dict[str, Any]]: Health score and detailed metrics dictionary.
    """
    if df is None or df.empty:
        return 0, {"missing_pct": 100, "duplicate_pct": 100, "total_rows": 0}

    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    missing_pct = (missing_cells / total_cells) * 100 if total_cells > 0 else 0

    total_rows = len(df)
    duplicate_rows = df.duplicated().sum()
    duplicate_pct = (duplicate_rows / total_rows) * 100 if total_rows > 0 else 0

    # Score deduction algorithm
    health_score = 100.0
    health_score -= missing_pct * 1.5  # Heavy penalty for missing data
    health_score -= duplicate_pct * 2.0  # Heavy penalty for exact duplicate rows

    health_score = max(0, min(100, int(round(health_score))))

    details = {
        "missing_pct": round(missing_pct, 2),
        "duplicate_pct": round(duplicate_pct, 2),
        "total_rows": total_rows,
        "total_cols": len(df.columns),
        "missing_cells": int(missing_cells),
        "duplicate_rows": int(duplicate_rows),
    }

    return health_score, details


def get_column_type_breakdown(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Categorizes dataframe columns into numerical, categorical, datetime, and boolean.
    
    Args:
        df (pd.DataFrame): Source DataFrame.
        
    Returns:
        Dict[str, List[str]]: Categorized column lists.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    datetime_cols = df.select_dtypes(include=["datetime64", "datetimetz"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    boolean_cols = df.select_dtypes(include=["bool"]).columns.tolist()

    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols,
        "boolean": boolean_cols,
    }


def aggregate_time_series(
    df: pd.DataFrame, date_col: str, value_col: str, freq: str = "D"
) -> pd.DataFrame:
    """
    Resamples time-series data to a specified frequency ('D' for Daily, 'W' for Weekly,
    'M' for Monthly, 'Q' for Quarterly) for time-series aggregation and forecasting.
    
    Args:
        df (pd.DataFrame): Source DataFrame.
        date_col (str): Column containing date values.
        value_col (str): Column to aggregate (e.g., Sales).
        freq (str): Resampling frequency string.
        
    Returns:
        pd.DataFrame: Aggregated time-series DataFrame indexed by date.
    """
    try:
        temp_df = df.copy()
        temp_df[date_col] = pd.to_datetime(temp_df[date_col])
        resampled = (
            temp_df.set_index(date_col)[value_col]
            .resample(freq)
            .sum()
            .reset_index()
            .sort_values(by=date_col)
        )
        return resampled
    except Exception as e:
        logger.error(f"Failed to resample time series data: {str(e)}")
        return pd.DataFrame()


# =============================================================================
# 3. FILE EXPORT HELPERS (CSV, EXCEL)
# =============================================================================
def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """
    Converts a pandas DataFrame into a UTF-8 encoded CSV byte stream for downloading.
    
    Args:
        df (pd.DataFrame): Data frame to convert.
        
    Returns:
        bytes: UTF-8 encoded CSV bytes.
    """
    return df.to_csv(index=False).encode("utf-8")


def convert_df_to_excel(df: pd.DataFrame, sheet_name: str = "Data") -> bytes:
    """
    Converts a pandas DataFrame into an Excel file (.xlsx) byte stream using OpenPyXL.
    
    Args:
        df (pd.DataFrame): Data frame to convert.
        sheet_name (str): Name of the Excel worksheet.
        
    Returns:
        bytes: OpenPyXL generated Excel file buffer bytes.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    processed_data = output.getvalue()
    return processed_data


# =============================================================================
# 4. REUSABLE STREAMLIT UI COMPONENTS
# =============================================================================
def render_kpi_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    border_color: str = "#1E88E5",
) -> None:
    """
    Renders a clean, responsive, custom KPI Card using HTML & CSS inside Streamlit.
    
    Args:
        title (str): Metric label/title.
        value (str): Main metric value (e.g., "$124.5K").
        subtitle (str, optional): Sub-text or comparison metric (e.g., "+12.4% vs last month").
        border_color (str): Highlight border color hex string.
    """
    sub_html = f"<div class='kpi-subtitle'>{subtitle}</div>" if subtitle else ""
    html_code = f"""
    <div class="kpi-card" style="border-top: 4px solid {border_color};">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = "📌") -> None:
    """
    Renders a stylized gradient section header.
    
    Args:
        title (str): Header text title.
        icon (str): Emoji or character icon.
    """
    html_code = f"""
    <div class="section-header">
        {icon} {title}
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def display_data_health_badge(score: int) -> None:
    """
    Displays a color-coded data quality health indicator badge based on the health score.
    
    Args:
        score (int): Data health score (0 to 100).
    """
    if score >= 85:
        color = "#4CAF50"  # Green
        status = "Excellent Data Quality"
    elif score >= 65:
        color = "#FF9800"  # Orange
        status = "Moderate Data Quality (Needs Cleaning)"
    else:
        color = "#F44336"  # Red
        status = "Poor Data Quality (Requires Immediate Attention)"

    st.markdown(
        f"""
        <div style="background-color: {color}22; border-left: 5px solid {color}; padding: 12px 16px; border-radius: 6px; margin-bottom: 15px;">
            <span style="font-weight: 600; font-size: 1.1rem; color: {color};">Data Quality Score: {score}%</span>
            <span style="font-size: 0.9rem; color: #888; margin-left: 10px;">({status})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# 5. ERROR HANDLING DECORATOR
# =============================================================================
def safe_execute(default_return: Any = None):
    """
    Decorator to wrap complex functions in exception handlers and log errors gracefully
    without stopping the Streamlit application flow.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error executing {func.__name__}: {str(e)}", exc_info=True)
                st.error(f"An unexpected error occurred in `{func.__name__}`: {str(e)}")
                return default_return

        return wrapper

    return decorator
