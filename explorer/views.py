from django.http import JsonResponse
import os
import json
import random


DUMMY_FILESYSTEM_PATH = os.path.join(os.path.dirname(__file__), "dummy_filesystem.json")

try:
    with open(DUMMY_FILESYSTEM_PATH, "r") as file:
        dummy_filesystem = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    dummy_filesystem = []

def get_directory_structure(request):
    """
    Returns the dummy file system structure in the expected format.
    """
    return JsonResponse(dummy_filesystem, safe=False)


def get_file_content(request, file_path):
    """
    Retrieves file or directory content based on the given file path.
    """
    parts = file_path.strip("/").split("/")

    def find_node(filesystem, parts, current_path=""):
        """Recursively search for a file or directory node."""
        for item in filesystem:
            if item["name"] == parts[0]:
                full_path = os.path.join(current_path, item["name"])
                if len(parts) == 1:
                    return item, full_path
                elif item["is_dir"]:
                    return find_node(item["children"], parts[1:], full_path)
        return None, ""

    node, full_path = find_node(dummy_filesystem, parts)

    if node is None:
        return JsonResponse({"error": f"Path '{file_path}' not found"}, status=404)

    def build_file_info(file_node, path_prefix):
        ext = os.path.splitext(file_node["name"])[1]
        return {
            "path": os.path.join(path_prefix, file_node["name"]),
            "type": "file",
            "file_type": "text/plain",
            "extension": ext,
            "name": file_node["name"],
            "size": random.randint(100, 1000)
        }

    def build_directory_info(dir_node, path_prefix):
        return {
            "path": path_prefix,
            "type": "directory",
            "name": dir_node["name"],
        }

    if node["is_dir"]:
        contents = []
        for child in node.get("children", []):
            child_path = os.path.join(full_path, child["name"])
            if child["is_dir"]:
                contents.append({
                    "path": child_path,
                    "type": "directory",
                    "name": child["name"],
                })
            else:
                contents.append(build_file_info(child, full_path))
        return JsonResponse({"type": "directory", "contents": contents})

    # For file node
    file_info = build_file_info(node, os.path.dirname(full_path))
    return JsonResponse({
        "type": "file",
        "content": file_info
    })
