# import importlib
# import os
# import csv
# from datetime import datetime
# from pathlib import Path
# import asyncio
# from asyncer import asyncify

# this_dir = Path(os.getcwd())
# PARSERS_DIR = "source_scripts"

# # This function collects results from both sync and async parse functions
# async def collect_results():
#     all_results = []
    
#     for script in os.listdir(PARSERS_DIR):
#         if script.endswith(".py"): 
#             script_name = script[:-3]
#             module_path = f"{PARSERS_DIR}.{script_name}"
#             try:
#                 module = importlib.import_module(module_path)
                
#                 # Handle synchronous parsing function
#                 if hasattr(module, "sync_parse"):
#                     print(f"Running sync_parse from {script_name}...")
#                     results = await asyncify(module.sync_parse())   # Call sync_parse as an async
#                     all_results.extend(results)
                
#                 # Handle asynchronous parsing function
#                 elif hasattr(module, "async_parse"):
#                     print(f"Running async_parse from {script_name}...")
#                     results = await module.async_parse()  # Use await to handle async_parse
#                     all_results.extend(results)
                
#                 else:
#                     print(f"No parse function found in {script_name}")
            
#             except Exception as e:
#                 print(f"Failed to import or run parser in {script_name}: {e}")
    
#     return all_results

# def save_results_to_csv(results):
#     # Create the results folder if it doesn't exist
#     this_dir.joinpath("results").mkdir(parents=True, exist_ok=True)

#     # Generate CSV file name based on current timestamp
#     timestamp="latest"
#     csv_file = f"results/parsed_results_{timestamp}.csv"
    
#     # Define CSV header based on result structure
#     header = ['title', 'link', 'deadline']

#     # Write the results to CSV file
#     with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=header)
#         writer.writeheader()
#         for row in results:
#             writer.writerow(row)

#     print(f"Results saved to {csv_file}")

# async def main():
#     # Run the async collection and then save the results
#     parsed_results = await collect_results()  # Await the async collect_results

#     # Save the results to a CSV file
#     save_results_to_csv(parsed_results)

# if __name__ == "__main__":
#     # Detect if the current event loop is already running, if so use create_task
#     try:
#         asyncio.run(main())  # Use asyncio to run async code
#     except RuntimeError as e:
#         if "asyncio.run() cannot be called from a running event loop" in str(e):
#             loop = asyncio.get_event_loop()
#             loop.create_task(main())
#         else:
#             raise
