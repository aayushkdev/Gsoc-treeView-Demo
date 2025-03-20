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
    dummy_filesystem = [] 

def get_directory_structure(request):
    """
    Returns the dummy file system structure in the expected format.
    """
    return JsonResponse(dummy_filesystem, safe=False)


def get_file_content(request, file_path):
    """
    Retrieves file content based on the given file path.
    """
    logger.debug(f"Requested file path: {file_path}")

    # Normalize the path
    parts = file_path.strip("/").split("/")
    
    def find_node(filesystem, parts):
        """Recursively search for a file or directory node."""
        for item in filesystem:
            if item["name"] == parts[0]:
                if len(parts) == 1:  
                    return item
                elif item["is_dir"]:  
                    return find_node(item["children"], parts[1:])
        return None

    node = find_node(dummy_filesystem, parts)

    if node is None:
        return JsonResponse({"error": f"Path '{file_path}' not found"}, status=404)

    if node["is_dir"]:
        return JsonResponse({"type": "directory", "contents": node["children"]})

    return JsonResponse({"type": "file", "content": node.get("content", "No content available.")})
