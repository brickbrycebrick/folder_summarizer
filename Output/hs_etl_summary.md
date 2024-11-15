# Folder Structure

## logs
## run.py
        - PipelineRunner: Orchestrates the running of the entire ETL pipeline.
            - __init__: Initialize the pipeline runner with common components.
            - run_etl: Run the ETL pipeline.
            - run_associations: Run the association processing.
            - run_full_pipeline: Run the complete pipeline including ETL and associations.
            - main: Main execution function.
## src
### __pycache__
### association_manager.py
        - HubSpotAssociationManager: Manages HubSpot object associations and their synchronization with the database.

    This class handles the extraction, processing, and storage of associations between
    different HubSpot objects. It uses batch processing to efficiently handle large
    numbers of associations and provides functionality to validate object types,
    process associations in batches, and save the results to a database.

    Attributes:
        MAX_BATCH_SIZE (int): Maximum number of IDs to process in a single batch.
        hubspot (HubSpotConnector): Connector for interacting with the HubSpot API.
        db (DatabaseManager): Manager for database operations.
        config (AssociationConfig): Configuration for association processing.

    Methods:
        process_all_associations(): 
            Process all configured associations.
        
        save_association_metadata(): 
            Save metadata about processed associations.
        
        _process_batch(from_object, to_object, batch_ids): 
            Process a single batch of IDs.
        
        _get_object_ids(table_name): 
            Retrieve HubSpot object IDs from the database table.
        
        _extract_associations(from_object, to_object): 
            Extract all associations between two HubSpot objects.
        
        _validate_object_types(from_object, to_object): 
            Validate that both objects exist in HubSpot.
        
        _save_associations_to_db(associations, from_object, to_object): S
            ave associations to the database.

    The class uses batch processing and error handling to manage large-scale association
    synchronization between HubSpot and a local database.
            - __init__: Process a single batch of IDs.
            - _process_batch: Process a single batch of IDs.
            - _get_object_ids: Retrieve HubSpot object IDs from the database table.
            - _extract_associations: Extract all associations between two HubSpot objects with batch processing.
            - process_all_associations: Process all configured associations.
            - _validate_object_types: Validate that both objects exist in HubSpot and are properly named.
            - _save_associations_to_db: Save associations to the database.
            - process_all_associations: Process all configured associations.
            - save_association_metadata: Save metadata about processed associations.
            - main: Main function to run the association processing.
### connectors.py
        - HubSpotConnector: Handles all HubSpot API interactions.

    This class provides methods to interact with the HubSpot API, including 
    retrieving object types, validating objects, fetching records, and managing 
    column information.

    Attributes:
        client (HubSpot): The HubSpot client instance.
        valid_objects (List[str]): List of valid HubSpot object types.

    Methods:
        __init__(access_token: str, portal_id: str):
            Initializes the HubSpot connector with the given access token and portal ID.

        _get_valid_object_types() -> List[str]:
            Returns a list of valid HubSpot object types, including both standard and custom objects.

        get_custom_obj_names() -> List[str]:
            Retrieves and returns a list of all custom objects in the CRM.

        validate_object_type(object_name: str) -> bool:
            Validates if the requested object type exists in HubSpot.

        get_column_dict(object_name: str) -> Dict[str, str]:
            Returns a dictionary of column names and labels for a specified HubSpot object.

        get_records(object_name: str, columns: List[str], cutoff_date: datetime.datetime) -> pd.DataFrame:
            Retrieves records from HubSpot for the specified object and columns, created after the cutoff date.

        get_validated_columns(object_name: str, desired_columns: List[str]) -> List[str]:
            Validates and returns column names that exist in HubSpot for the specified object.
            - __init__: Initialize HubSpot connector.
        
        Args:
            access_token (str): HubSpot API access token
            portal_id (str): HubSpot portal ID
            - _get_valid_object_types: Returns a list of valid HubSpot object types.
            - get_custom_obj_names: Returns a list of all custom objects in the CRM.
            - validate_object_type: Validates if the requested object type exists in HubSpot.
        
        Args:
            object_name (str): Name of the HubSpot object
            
        Returns:
            bool: True if object exists, False otherwise
            - get_column_dict: Returns a dictionary of column names and labels for a HubSpot object.
            - get_records: Retrieves records from HubSpot for specified object and columns.
            - get_validated_columns: Validates and returns column names that exist in HubSpot.
            
        - DatabaseManager: Handles database operations.

    This class provides methods to interact with a database, including 
    connection management, query execution, and data writing operations.

    Attributes:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine for database operations.

    Methods:
        __init__(connection_string: str):
            Initializes the DatabaseManager with the given connection string.

        _execute_with_retry(query: str, max_retries: int = 3) -> None:
            Executes a SQL query with retry logic in case of transaction rollbacks.

        _check_table_exists(table_name: str) -> bool:
            Checks if a table exists in the database.

        write_to_db(df: pd.DataFrame, table_name: str, chunk_size: Optional[int] = 1000, replace_table: bool = True) -> None:
            Writes a DataFrame to a database table with support for chunking and table replacement.

    The class uses SQLAlchemy for database operations and includes error handling
    and logging for robustness.
            - __init__: Initialize database connection with proper error handling.
            - _execute_with_retry: Execute a SQL query with retry logic.
            - _check_table_exists: Check if a table exists in the database.
            - write_to_db: Writes dataframe to database table with improved error handling and chunking.
        
        Args:
            df (pd.DataFrame): DataFrame to write
            table_name (str): Name of the target table
            chunk_size (int, optional): Number of rows to write at once. None for no chunking
            replace_table (bool): If True, replaces existing table. If False, appends to it

...
