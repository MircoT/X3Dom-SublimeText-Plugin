X3Dom-SublimeText-Plugin
========================

Thi is a plugin for Sublime Text which helps to write X3Dom projects. This plugin provide some
resources to write easily X3Dom files, currently only completion and snippet code are implemented
(I'd like to add syntax checking). It works on HTML plugin scope, so you can open an html page 
with Sublime Text without change language to see X3Dom's tags suggestion.

# Installation

In the future can be added via [Package Control](http://wbond.net/sublime_packages/package_control) manager.  


At the moment you must clone the git repository directly inside your Sublime "Packages" directory.

```git clone https://github.com/MircoT/X3Dom-SublimeText-Plugin.git "X3Dom"```

This way, you'll be able to "git pull" to update the package, and Sublime will see the changes immediately. You can use the Preferences>Browse Packages menu within Sublime to get to the Packages directory.

Otherwise, clone elsewhere and copy the files into a folder called "E2D-Script" in the Packages directory.

# How to use it

This plugin is **under development**, so the tags that you can access now are only a few, but you can add tags
easily.

For nodes' specifics you can go here: [X3Dom Doc Nodes](http://x3dom.org/docs/dev/nodes/index.html).
You can add X3Dom tags editing **tags.json** (there are few sample tags in this file).
If you respect the category's subdivision, a pull request with corrected tags is appreciated
(I don't have much time right now to add all the nodes).  

After that you can click on *Refresh X3Dom Plugin* to update the tags list.
The refresh adds new entries on X3Dom menu both on ```Tools -> X3Dom``` and ```Right click -> X3Dom```.
It also adds snippet codes, so you can use autocompletion with tab key and search completion like on html files.  

To see the project (web page) in the browser you can use [View in Browser](https://github.com/adampresley/sublime-view-in-browser) plugin
for Sublime Text.

# License

The MIT License (MIT)

Copyright (c) 2013 Mirco

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
