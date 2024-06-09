import os
import shutil

from html_template import index_template, carousel_template
from markdown_to_html import split_markdown_text, markdown_to_html

CONTENT_DIR = "./content"
EXCLUDED_FOLDERS = ["content", ".git", "src", ".mypy_cache"]

# import sys
# import markdown

# markdown_text = """
# # Heading
# - List item 1
# - List item 2
# """

# html = markdown.markdown(markdown_text)
# print(html)


# print(sys.executable)


def rec_list_folders_in_dir(dir):
    folders = []
    for folder in os.listdir(dir):
        folder_path = os.path.join(dir, folder)
        if os.path.isdir(folder_path):
            folders.append(folder_path)
            folders.extend(rec_list_folders_in_dir(folder_path))
    return folders


def move_up_one_dir(path):
    new_path = path.replace(CONTENT_DIR, ".")
    if new_path != ".":
        # print(f"deleting {new_path}")
        shutil.rmtree(new_path, ignore_errors=True)
    # if not os.path.exists(new_path):
    os.makedirs(new_path, exist_ok=True)
    print(f"Created directory: {new_path}")
    return new_path


def not_excluded_folder(folder):
    return folder not in EXCLUDED_FOLDERS


def first_dirname(path):
    return os.path.basename(os.path.dirname(path))


path = "."  # "content/programming-syntax/variables"


def write_index_html(path, title="Programming Syntax Flashcards"):
    hirearchy = [x.title() for x in path.split("/")[1:]]
    if len(hirearchy) > 0:
        title = title + " - " + " - ".join(hirearchy)
    folder_names = [
        name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))
    ]
    folder_names = list(filter(not_excluded_folder, folder_names))
    links = [
        {"href": f"./{folder}/", "text": folder.replace("-", " ").title()}
        for folder in folder_names
    ]
    context = {
        "title": title,
        "links": links,
    }
    html_output = index_template.render(context)
    index_file_path = os.path.join(path, "index.html")
    with open(index_file_path, "w") as index_file:
        index_file.write(html_output)
        print(f"Created index.html in: {path}")


def write_carousel_html(md_folder, path, title="Programming Syntax Flashcards"):
    hirearchy = [x.title() for x in path.split("/")[1:]]
    if len(hirearchy) > 0:
        title = title + " - " + " - ".join(hirearchy)
    markdown_files = [name for name in os.listdir(md_folder) if name.endswith(".md")]
    slides = []
    for markdown_file in markdown_files:
        with open(os.path.join(md_folder, markdown_file)) as file:
            markdown_text = file.read()
            text, code = split_markdown_text(markdown_text)
            slide = {"text": markdown_to_html(text), "code": markdown_to_html(code)}
            slides.append(slide)
    context = {
        "title": title,
        "slides": slides,
    }
    html_output = carousel_template.render(context)
    carousel_file_path = os.path.join(path, "index.html")
    with open(carousel_file_path, "w") as carousel_file:
        carousel_file.write(html_output)
        print(f"Created index.html in: {path}")


def contains_md_files(folder):
    for file in os.listdir(folder):
        if file.endswith(".md"):
            return True
    return False


def main():
    folders = rec_list_folders_in_dir(CONTENT_DIR)
    print(f"folders: {folders}")
    if os.path.exists("./index.html"):
        os.remove("./index.html")
    write_index_html(".")
    new_paths = []
    for folder in folders:
        if contains_md_files(folder):
            new_path = move_up_one_dir(folder)
            write_carousel_html(folder, new_path)
        else:
            new_paths.append(move_up_one_dir(folder))
    for new_path in new_paths:
        write_index_html(new_path)


if __name__ == "__main__":
    main()

# Todo: Code syntax highlighting
