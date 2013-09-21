import sublime, sublime_plugin
import json
import os

X3D_COMPLETIONS_BASE = """import sublime, sublime_plugin

# Provide completions that match just after typing an opening angle bracket
class MyTagCompletions(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        # Only trigger within HTML
        if not view.match_selector(locations[0],
                "text.html"):
            return []

        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))
        if ch != '<':
            return []

        completions =  [
%s
        ]

        return (sorted(completions), sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS)"""

X3Dom_BASE = """import sublime, sublime_plugin

X3D_BASE_TEMPLATE = \"\"\"<!DOCTYPE html>
<html>
    <head>
        <meta encoding="utf-8">
        <script src="http://www.x3dom.org/download/dev/x3dom.js"></script>
        <script src="http://www.x3dom.org/download/dev/x3dom.swf"></script>
        <link rel="stylesheet" href="http://www.x3dom.org/download/dev/x3dom.css">
    </head>
    <body>
        <x3d xmlns="http://www.x3dom.org/x3dom" showStat="false" showLog="false" width="800px" height="600px">
            <scene>
                $1
            </scene>
        </x3d>
    </body>
</html>
\"\"\"

X3D_TAGS_CONTENTS = {
%s
}

class Newx3dprojectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Clear view
        self.view.erase(edit, sublime.Region(0, self.view.size()))
        # Insert text from cursor
        #self.view.insert(edit, self.view.sel()[0].begin(), BASE_X3D) #OLD
        # Insert snippet
        self.view.run_command('insert_snippet', dict(contents=X3D_BASE_TEMPLATE))

class Insertx3dtagCommand(sublime_plugin.TextCommand):
    def run(self, edit, tag=None):
        if tag is not None:
            self.view.run_command('insert_snippet', dict(contents=X3D_TAGS_CONTENTS[tag]))"""

def Gen_attributes(tag_contents):
    """Create snippet code for attributes
    """
    num_val = 1
    string = ""
    for attribute, values in sorted(tag_contents.items()):
        string += attribute + "=\\\""
        for value in values:
            string += "${%s:%s}" % (num_val, value)
            if len(values) != 1:
                string += " "
            num_val += 1
        if string[-1] == " ":
            string = string[:-1]
        string += "\\\""
        if len(attribute) != 1:
            string += " "
    if string[-1] == " ":
        string = string[:-1]
    return string

def Gen_Insertx3dtagCommand_entry(tag_name, tag_contents):
    """Generate Gen_Insertx3dtagCommand string
    """
    string = "<%s " % tag_name
    string += Gen_attributes(tag_contents)
    string += "></%s>" % tag_name
    return string

def Gen_all_x3dtagCommand(tags):
    """Generate X3Dom.py file
    """
    tab = " "*4
    completion_string = ""
    for cat, nodes in sorted(tags.items()):
        completion_string += tab + "# Category %s\n" % cat
        for node, attrs in sorted(nodes.items()):
            completion_string += tab + "'%s': \"%s\"" % (node, Gen_Insertx3dtagCommand_entry(node, attrs))
            completion_string += ",\n"
    completion_string = completion_string[:-2]
    with open("X3Dom.py", "w") as fp:
        fp.write(X3Dom_BASE % completion_string)

def Gen_completion_entry(tag_name, tag_contents, category, tab=" "*12):
    """Generate completion string
    """
    string = tab + "(\"%s\\t%s - X3D Tag\", \"%s " % (tag_name, category, tag_name)
    string += Gen_attributes(tag_contents)
    string += "></%s>\")" % tag_name
    return string

def Gen_all_completions(tags):
    """Generate html_x3d_completions.py file
    """
    tab = " "*12
    completion_string = ""
    for cat, nodes in sorted(tags.items()):
        completion_string += tab + "# Category %s\n" % cat
        for node, attrs in sorted(nodes.items()):
            completion_string += Gen_completion_entry(node, attrs, cat) + ",\n"
    completion_string = completion_string[:-2]
    with open("html_x3d_completions.py", "w") as fp:
        fp.write(X3D_COMPLETIONS_BASE % completion_string)

def Gen_snippet_entry(tag_name, tag_contents):
    """Generate snippet string
    """
    string = "<snippet>\n\t<content>\n\t\t<![CDATA[<%s " % tag_name
    string += Gen_attributes(tag_contents).replace("\\\"", "\"")
    string += "></%s>" % tag_name
    string += "]]>\n\t</content>\n"
    string += "\t<tabTrigger>&lt;%s</tabTrigger>\n" % tag_name
    string += "\t<scope>text.html</scope>\n</snippet>"
    return string

def Gen_all_snippets(tags):
    """Generate a snippet file for every tag
    and deletes all previous snippet files
    """
    dir_snippets = os.path.abspath(os.path.join(os.path.dirname(__file__), "X3D_Snippets"))
    for file_path in os.listdir(dir_snippets):
        os.remove(os.path.join(dir_snippets, file_path))
    # Generate all files for all categories
    for cat, nodes in sorted(tags.items()):
        for node, attrs in sorted(nodes.items()):
            with open(dir_snippets + "/x3d.%s.sublime-snippet" % node, "w") as fp:
                fp.write(Gen_snippet_entry(node, attrs))

def Gen_menu_entry(tag_name):
    """Generate a part of json file as a python dict
    """
    tag_dict = dict()
    tag_dict["caption"] = tag_name
    tag_dict["command"] = "insertx3dtag"
    tag_dict["args"] = {"tag": tag_name}
    return tag_dict

def Gen_all_menu(tags):
    """Generate all menu files
    """
    context_menu = list()
    main_menu = list()
    # Context menu init
    context_menu.append(
        {
            'caption': "-",
            'id': "side-bar-end-separator"
        }
    )
    context_menu.append(
        {
            'caption': "X3Dom",
            'children': list()
        }
    )
    context_menu[1]['children'].append(
        {
            'caption': "Refresh X3Dom plugin",
            'command': "genx3domfiles"
        }
    )
    context_menu[1]['children'].append(
        {
            'caption': "Edit X3Dom tags",
            'command': "editx3domtags"
        }
    )
    context_menu[1]['children'].append(
    {
            'caption': "-",
            'id': "side-bar-end-separator"
        }
    )
    context_menu[1]['children'].append(
        {
            'caption': "New X3Dom Project",
            'command': "newx3dproject"
        }
    )
    context_menu[1]['children'].append(
        {
            'caption': "-",
            'id': "side-bar-end-separator"
        }
    )
    # Main menu init
    main_menu.append(
        {
            'id': "tools",
            'children': list()
        }
    )
    main_menu[0]['children'].append(
        {
            'caption': "X3Dom",
            'children': list()
        }
    )
    main_menu[0]['children'][0]['children'].append(
        {
            'caption': "Refresh X3Dom plugin",
            'command': "genx3domfiles"
        }
    )
    main_menu[0]['children'][0]['children'].append(
        {
            'caption': "Edit X3Dom tags",
            'command': "editx3domtags"
        }
    )
    main_menu[0]['children'][0]['children'].append(
        {
            'caption': "-",
            'id': "side-bar-end-separator"
        }
    )
    main_menu[0]['children'][0]['children'].append(
        {
            'caption': "New X3Dom Project",
            'command': "newx3dproject"
        }
    )
    main_menu[0]['children'][0]['children'].append(
        {
            'caption': "-",
            'id': "side-bar-end-separator"
        }
    )
    for cat, nodes in sorted(tags.items()):
        new_category = dict()
        new_category['caption'] = cat
        new_category['children'] = list()
        for node in sorted(nodes.keys()):
            new_category['children'].append(Gen_menu_entry(node))
        context_menu[1]['children'].append(new_category)
        main_menu[0]['children'][0]['children'].append(new_category)

    # Generate files
    file_path_context = os.path.abspath(os.path.join(os.path.dirname(__file__), "Context.sublime-menu"))
    with open(file_path_context, "w") as fp:
        fp.write(json.dumps(context_menu, indent=4))
    file_path_main = os.path.abspath(os.path.join(os.path.dirname(__file__), "Main.sublime-menu"))
    with open(file_path_main, "w") as fp:
        fp.write(json.dumps(main_menu, indent=4))

class Genx3domfilesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        tags = dict()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "tags.json"))
        with open(file_path, "r") as fp:
            tags = json.load(fp)
        sublime.status_message("X3Dom Plugin starts to create all files...")
        Gen_all_menu(tags)
        Gen_all_snippets(tags)
        Gen_all_completions(tags)
        Gen_all_x3dtagCommand(tags)
        sublime.status_message("!!! End process!!!")

class Editx3domtagsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.window().open_file("tags.json")
        sublime.status_message("Opened X3Dom tags file!")