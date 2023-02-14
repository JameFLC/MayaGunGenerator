from __future__ import absolute_import
import os
import random
import maya.cmds as mc
from pathlib import Path

GROUP_NAME = "gun_grp"
RELATIVE_PATH: str = "~/maya/2022/scripts/procedural_guns/ressources/models"
MAX_SEED_NUMBER = 999999
part_options = {
    "accessory": True,
    "barrel": True,
    "body": True,
    "body": True,
    "gripp": True,
    "magazine": True,
    "sight": True,
    "stock": True
}


def generate_gun(seed: int = 0):

    seed = hash_seed(seed)
    print(f"Seed used {seed} with options {part_options}")
    clear_gun()
    gun_grp: str = mc.createNode("transform", name=GROUP_NAME)

    if not part_options["body"]:
        return
    # Body Import

    body_ref = import_part("bodies", seed)
    body = get_transform_node_ref(body_ref)
    body = mc.parent(body, gun_grp)[0]

    seed = hash_seed(seed)
    # Part Imports
    stock_ref, stock, stock_transform = SetupPart(
        "stock", seed, part_options["stock"])

    seed = hash_seed(seed)

    gripp_ref, gripp, gripp_transform = SetupPart(
        "gripp", seed, part_options["gripp"])

    seed = hash_seed(seed)

    sight_ref, sight, sight_transform = SetupPart(
        "sight", seed, part_options["sight"])

    seed = hash_seed(seed)

    magazine_ref, magazine, magazine_transform = SetupPart(
        "magazine", seed, part_options["magazine"])

    seed = hash_seed(seed)

    barrel_ref, barrel, barrel_transform = SetupPart(
        "barrel", seed, part_options["barrel"])

    # Accessory Import
    if part_options["accessory"]:
        accessory_ref = import_part(f"accessories", seed)
        accessory = get_transform_node_ref(accessory_ref)

        accessory_transforms: list[str] = mc.ls(f"*_accessory*")

        accessory_transforms = filter(accessory_transforms, "RN")
    if part_options["barrel"]:
        accessory_transform = mc.ls(f"*_accessory")[0]

    if part_options["accessory"]:
        snap_translates(accessory, accessory_transform)

    # Convertion from ref to meshes
    make_reference_editable(body_ref)

    if part_options["stock"]:
        make_reference_editable(stock_ref)
    if part_options["gripp"]:
        make_reference_editable(gripp_ref)
    if part_options["sight"]:
        make_reference_editable(sight_ref)
    if part_options["magazine"]:
        make_reference_editable(magazine_ref)
    if part_options["barrel"]:
        make_reference_editable(barrel_ref)
    if part_options["accessory"]:
        make_reference_editable(accessory_ref)

    # Reparenting
    if part_options["stock"]:
        stock = mc.parent(stock, body)[0]
    if part_options["gripp"]:
        gripp = mc.parent(gripp, body)[0]
    if part_options["sight"]:
        sight = mc.parent(sight, body)[0]
    if part_options["magazine"]:
        magazine = mc.parent(magazine, body)[0]
    if part_options["barrel"]:
        barrel = mc.parent(barrel, body)[0]
    if part_options["accessory"]:
        accessory = mc.parent(accessory, barrel)[0]
    # Empty deletions
    if part_options["body"]:
        mc.delete(stock_transform)
        mc.delete(gripp_transform)
        mc.delete(sight_transform)
        mc.delete(magazine_transform)
        mc.delete(barrel_transform)
    if part_options["barrel"]:
        mc.delete(accessory_transform)

    mc.select(deselect=True)


def hash_seed(seed: int) -> int:
    return hash(seed) % MAX_SEED_NUMBER


def SetupPart(part_type: str, seed: int, used: bool):
    part_ref = import_part(f"{part_type}s", seed) if used else ""
    part = get_transform_node_ref(part_ref) if used else ""

    part_transforms = mc.ls(f"*_{part_type}FBXASC046001")

    if len(part_transforms) == 0:
        part_transforms = mc.ls(f"*_{part_type}")

    if used:
        snap_translates(part, part_transforms[0])
    return part_ref, part, part_transforms[0]


def make_reference_editable(ref: str):
    mc.file(ref, ir=True)


def get_transform_node_ref(ref_file):
    nodes = [n for n in mc.referenceQuery(
        ref_file, nodes=True) if mc.nodeType(n) == "transform"]
    node = nodes[0]
    return node


def clear_gun():
    for f in mc.file(q=True, r=True):
        mc.file(f, removeReference=True)
    mc.delete(mc.ls(GROUP_NAME))
    mc.clearCache(all=True)


def get_models_path() -> str:
    path: str = os.path.expanduser(RELATIVE_PATH)
    exist = os.path.exists(path)
    if not exist:
        print("path does not exist")
    return path


def import_part(part_type: str, index: int = 0):
    files = get_part_list(part_type)
    file: str = files[index % (len(files))]
    file_path = get_models_path() + r"/" + part_type + r"/" + file

    file_path = rf"{Path(file_path)}"

    return mc.file(file_path, reference=True)


def get_part_list(part_type: str) -> str:
    str_part_path = get_models_path() + "/" + part_type + "/"

    files: list[str] = []

    for file in os.listdir(str_part_path):
        if file.endswith(".mb"):
            files.append(file)
    return files


def snap_translates(object_to_move, target_object):
    target_object_matrix: list[float] = mc.getAttr(
        f"{target_object}.worldMatrix[0]")
    object_to_move_matrix: list[float] = mc.getAttr(
        f"{object_to_move}.worldMatrix[0]")

    # Filter out translate component
    object_to_move_matrix = object_to_move_matrix[:-3]
    # Filtenr in translate component
    target_object_matrix = target_object_matrix[len(target_object_matrix)-3:]

    moved_object_matrix = object_to_move_matrix + target_object_matrix

    mc.xform(object_to_move, worldSpace=True, matrix=moved_object_matrix)
