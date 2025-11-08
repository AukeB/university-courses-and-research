""" """

from typing import Any, Union
from ruamel.yaml.comments import CommentedMap, CommentedSeq  # type: ignore


def format_for_writing_to_yaml_file(  # type: ignore[no-untyped-def]
    obj: Union[dict, list, Any], path=None
) -> Union[CommentedMap, CommentedSeq, Any]:
    """
    Recursively format a dict/list for ruamel.yaml export.
    RGB color lists in window.background_color and map.colors are forced inline.
    """
    path = path or []

    if isinstance(obj, dict):
        new_map = CommentedMap()
        for k, v in obj.items():
            new_map[k] = format_for_writing_to_yaml_file(v, path + [k])

        # Add spacing between top-level keys for readability
        if not path:
            keys = list(new_map.keys())
            for k in keys[1:]:
                new_map.yaml_set_comment_before_after_key(k, before="\n")

        return new_map

    elif isinstance(obj, list):
        # Force inline for RGB color lists
        # window.background_color
        if path == ["window", "background_color"]:
            seq = CommentedSeq()
            for item in obj:
                seq.append(item)
            seq.fa.set_flow_style()  # Force inline
            return seq

        # map.colors.<color_name>
        if (
            len(path) >= 3
            and path[0] == "map"
            and path[1] == "colors"
            and path[2]
            in ["wall", "clean_floor", "stain", "vacuum_cleaner", "grid_lines"]
        ):
            seq = CommentedSeq()
            for item in obj:
                seq.append(item)
            seq.fa.set_flow_style()  # Force inline
            return seq

        # Otherwise, default: block style
        seq = CommentedSeq()
        for item in obj:
            seq.append(format_for_writing_to_yaml_file(item, path))
        return seq

    else:
        return obj
