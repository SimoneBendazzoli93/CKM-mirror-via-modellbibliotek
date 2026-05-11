import requests
import pandas as pd
BASE_URL = "https://ehrbase.maia.dsp.se"
AUTH = ("ehrbase-admin", "EvenMoreSecretPassword") 

# 1. Use AQL to find all EHR IDs
print("Searching for all EHR IDs using AQL...")

# This is the SQL equivalent of "SELECT id FROM patients"
aql_query = "SELECT e/ehr_id/value FROM EHR e"

query_response = requests.get(
    f"{BASE_URL}/ehrbase/rest/openehr/v1/query/aql",
    params={"q": aql_query},
    headers={"Accept": "application/json"},
    auth=AUTH,
    verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt"
)

if query_response.status_code == 200:
    # AQL results come back in a "rows" array
    results = query_response.json().get("rows", [])
    
    if not results:
        print("No EHRs found. The database is already clean!")
    else:
        print(f"Found {len(results)} EHR(s). Wiping them via Admin API...")
        
        # 2. Loop through and delete each EHR using the Admin API
        for row in results:
            ehr_id = row[0]
            # Use this for a "Deep Dive" into every single data point in the EHR
            aql_flattened = (
                f"SELECT "
                f"c/uid/value as composition_id, "
                f"e/name/value as field_name, "
                f"e/value as field_value "
                f"FROM EHR ehr [ehr_id/value='{ehr_id}'] "
                f"CONTAINS COMPOSITION c "
                f"CONTAINS ELEMENT e"
            )
            
            query_response = requests.get(
                f"{BASE_URL}/ehrbase/rest/openehr/v1/query/aql",
                params={"q": aql_flattened},
                headers={"Accept": "application/json"},
                auth=AUTH,
                verify="C:/Users/simon/OneDrive - Linköpings universitet/kube/maia-dsp/ca.crt"
            )
            output_file = f"EHR_{ehr_id}.xlsx"
            if query_response.status_code == 200:
                data = query_response.json()
                rows = data.get("rows", [])
                columns = [col["name"] for col in data.get("columns", [])]
                
                # 3. Process data into a DataFrame
                # AQL results are lists of lists, perfect for DataFrame construction
                # Transform 'field_value' if it's a dict with '_type' == 'DV_QUANTITY'
                def format_field_value(val):
                    if isinstance(val, dict) and val.get('_type') == 'DV_QUANTITY':
                        return f"{val.get('magnitude', '')} {val.get('units', '')}".strip()
                    elif isinstance(val, dict) and val.get('_type') == 'DV_CODED_TEXT':
                        return val.get('value', '')
                    elif isinstance(val, dict) and val.get('_type') == 'DV_TEXT':
                        return val.get('value', '')
                    elif isinstance(val, dict) and val.get('_type') == 'DV_DURATION':
                        return val.get('value', '')
                    return val
                
                

                # Process rows: modify 'field_value' in each row if needed
                # Find the column index for 'field_value'
                try:
                    field_value_idx = columns.index("field_value")
                except ValueError:
                    field_value_idx = None

                processed_rows = []
                for row in rows:
                    if field_value_idx is not None and len(row) > field_value_idx:
                        # Copy row to avoid mutating original data
                        new_row = list(row)
                        new_row[field_value_idx] = format_field_value(new_row[field_value_idx])
                        processed_rows.append(new_row)
                    else:
                        processed_rows.append(row)
                df = pd.DataFrame(processed_rows, columns=columns)

                # Rename columns to ID, Name, Value
                df.columns = ['ID', 'Name', 'Value']
         
                # 4. Save to Excel with formatting
                with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='EHR Data')
                    
                    # Simple formatting: auto-adjust column widths
                    ws = writer.sheets['EHR Data']
                    for col in ws.columns:
                        max_length = 0
                        column = col[0].column_letter
                        for cell in col:
                            try:
                                if len(str(cell.value)) > max_length:
                                    max_length = len(str(cell.value))
                            except: pass
                        ws.column_dimensions[column].width = max_length + 2
                        
                print(f"✅ Data exported successfully to {output_file}")
            else:
                print(f"❌ Query failed: {query_response.status_code}")
                
else:
    print(f"Failed to query EHRs. Status: {query_response.status_code}: {query_response.text}")