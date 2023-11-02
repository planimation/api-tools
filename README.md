# Access Planimation API

The Planimation API provides programmatic access to Planimation, an online PDDL problem solver and visualiser. Planimation with user interface can be accessed through [here]. A python library and a python-based command line utility are provided to easily access the API. They provide the same functionalities as the user interface.

### Installation
Simply fork this repository and you can have access to the source code. Unfortunately, there are no `pip` or `conda` installation options available at this stage.

### Python Library

The `planimation_api.py` library provides following methods:
Method | Description
------------ | -------------
`pddl_visualise(path of domain, path of problem, path of animation, output format, start step, end step, quality of animation)` | Submit 3 pddl files which corresponds to domain, problem, animation profile respectively and receive response in one of 5 supported formats (vfg, png, gif, webm, mp4). Similar to "Build visualisation from problem" on user interface. Additional parameters (optional): start step and end step of the animation range, quality (1 for low, 2 for medium, 3 for high).
`vfg_visualise(path of vfg, output format, start step, stop step, quality of animation)` | Submit a vfg file and receive response in one of 4 supported formats (png, gif, webm, mp4). Similar to "Build visualisation from solution VFG" on user interface. Additional parameters (optional): start step and end step of the animation range, quality (1 for low, 2 for medium, 3 for high).

An example of usage is demonstrated below:
```python
import planimation_api as api
result = api.pddl_visualise("domain.pddl", "problem.pddl", "ap.pddl", "mp4", 0, 20, 1)
# save the animation locally as 'animation.mp4'
with open('animation.mp4','wb') as animation:
    animation.write(result)
```
PNG animation will be returned as zip archive. An example of usage of PNG downloading is demonstrated below:
```python
import planimation_api as api
import zipfile
from io import BytesIO
result = api.pddl_visualise("domain.pddl", "problem.pddl", "ap.pddl", "png", 0, 20, 1)
# save png in a local folder named 'animation_png'
with zipfile.ZipFile(BytesIO(result), 'r') as zip_ref:
    zip_ref.extractall('animation_png')
```

### Command Line Utility

The `planimation.py` command-line utility provides exactly the same functionalities as the `planimation_api.py` library:

`submitPDDL` submits 3 pddl files which corresponds to domain, problem, animation profile respectively and receive response in one of 5 supported formats (vfg, png, gif, webm, mp4)
```sh
$ planimation.py submitPDDL <path of domain> <path of problem> <path of animation profile> <output format> --startStep [start step of animation] --stopStep [stop step of animation] --quality [quality of animation] 
```
`submitVFG` submits a vfg file and receive response in one of 4 supported formats (png, gif, webm, mp4)
```sh
$ planimation.py submitVFG  <path of VFG> <output format> --startStep [start step of animation] --stopStep [stop step of animation] --quality [quality of animation]                 
```

### Note for developer
The urls in `planimation_api.py` need to be changed to the actual urls in use.
https://github.com/planimation/api-tools/blob/bac3d948ffb7f0ceb6de389bf8f7dc38e57328be/planimation_api.py#L6-L8

### Warning
A malicious or careless user can easily spam requests using the python library and there is no mechanism at the server to handle such situation. Until relevant mechanism is implemented, it may not be safe to publish this python library.

### Thanks
The first version of Planimation API is developed by Changyuan Liu, Lingfeng Qiang, Mengyi Fan, Xinzhe Li and Zhaoqi Fang under Nir Lipovetzky's guidance.

The second version incorporating additional optional parameters is developed by Tim Bunnage, Wenxuan Zhang, Li Ching Tan, Junqi Ning and Xiaoyinzheng Ji with invaluable guidance from Nir Lipovetzky.

[//]: #
   [here]:<https://planimation.planning.domains/>
