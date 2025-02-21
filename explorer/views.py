from django.http import JsonResponse
import logging
import os
import json

logger = logging.getLogger(__name__)

DUMMY_FILESYSTEM_PATH = os.path.join(os.path.dirname(__file__), "dummy_filesystem.json")

try:
    with open(DUMMY_FILESYSTEM_PATH, "r") as file:
        dummy_filesystem = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Error loading dummy filesystem: {e}")
    dummy_filesystem = {}


# Helper function to get directory structure
def get_directory_structure(request):
    return JsonResponse(dummy_filesystem)

# Get file content from the dummy file system
def get_file_content(request, file_path):
    logger.debug(f"Requested file path: {file_path}")

    # Split path into parts
    parts = file_path.split("/")
    node = dummy_filesystem

    # Traverse the dummy file system
    try:
        for part in parts:
            node = node[part]  # Move to the next folder or file

        if isinstance(node, dict):
            return JsonResponse({"error": "This is a folder, not a file"}, status=400)

        return JsonResponse({"content": node})

    except KeyError:
        return JsonResponse({"error": "File not found"}, status=404)
