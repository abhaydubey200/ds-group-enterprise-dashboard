import streamlit as st
import snowflake.connector


def get_connection():
    """
    Returns a Snowflake connection using Streamlit secrets
    """

    try:
        conn = snowflake.connector.connect(
            account=st.secrets["snowflake"]["account"],
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            role=st.secrets["snowflake"]["role"],
            autocommit=True
        )
        return conn

    except Exception as e:
        # Hard fail: Snowflake must exist
        raise RuntimeError("❌ Snowflake connection failed. Check secrets.")
