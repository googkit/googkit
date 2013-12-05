import os
import shutil
import googkit.lib.path


def _mkdir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
        shutil.copymode(src, dst)
        shutil.copystat(src, dst)


def copytree(src, dst, ignore=None):
    """Same as os.shutil.copytree, but it can be used for a non-empty directory
    as dst.
    All subdirectories will be merged into existing ones.
    """
    _mkdir(src, dst)

    for src_root, src_dirs, src_files in os.walk(src):
        dst_root = googkit.lib.path.replace_base(src_root, src, dst)
        _mkdir(src_root, dst_root)

        if ignore is None:
            ignore_objs = []
        else:
            ignore_objs = ignore(src_root, src_dirs + src_files)

            # Remove ignored dirs
            for src_dir in src_dirs:
                if src_dir in ignore_objs:
                    src_dirs.remove(src_dir)

        for dir_name in src_dirs:
            if dir_name in ignore_objs:
                continue

            src_dir = os.path.join(src_root, dir_name)
            dst_dir = googkit.lib.path.replace_base(src_dir, src, dst)
            _mkdir(src_dir, dst_dir)

        for file_name in src_files:
            if file_name in ignore_objs:
                continue

            src_file = os.path.join(src_root, file_name)
            dst_file = googkit.lib.path.replace_base(src_file, src, dst)
            shutil.copy2(src_file, dst_file)
