<p align="left">
    <img src="https://raw.githubusercontent.com/aidudezzz/deepbots-swag/main/logo/deepbots_full.png">
</p>

[![Version](https://img.shields.io/pypi/v/deepbots?color=green)](https://pypi.org/project/deepbots/)
[![Dev Version](https://img.shields.io/github/v/tag/aidudezzz/deepbots?include_prereleases&label=test-pypi&color=green)](https://test.pypi.org/project/deepbots/)
[![Documentation Status](https://readthedocs.org/projects/deepbots/badge/?version=latest)](https://deepbots.readthedocs.io/en/latest/?badge=latest)
[![Downloads](https://static.pepy.tech/personalized-badge/deepbots?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/deepbots)
[![License](https://img.shields.io/github/license/aidudezzz/deepbots?color=green)](https://github.com/aidudezzz/deepbots/blob/dev/LICENSE)
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#contributors-)

Deepbots is a simple framework which is used as "middleware" between the free
and open-source [Cyberbotics' Webots](https://cyberbotics.com/) robot simulator
and Reinforcement Learning (RL) algorithms. When it comes to RL, 
[gym](https://www.gymlibrary.dev/) environments have been established 
as the most used interface between the actual application and the RL algorithm.

**Deepbots is a framework which follows the gym interface logic and bridges the 
gap between the gym environment and the simulator to enable you to easily 
create custom RL environments in Webots.**

## Installation

### Prerequisites

1. [Install Webots](https://cyberbotics.com/doc/guide/installing-webots)
   - [Windows](https://cyberbotics.com/doc/guide/installation-procedure#installation-on-windows)
   - [Linux](https://cyberbotics.com/doc/guide/installation-procedure#installation-on-linux)
   - [macOS](https://cyberbotics.com/doc/guide/installation-procedure#installation-on-macos)
2. [Install Python version 3.X](https://www.python.org/downloads/) (please
   refer to
   [Using Python](https://cyberbotics.com/doc/guide/using-python#introduction)
   to select the proper Python version for your system)
3. Refer to the [Using Python](https://cyberbotics.com/doc/guide/using-python)
   guide provided by Webots
4. Webots provides a basic code editor, but if you want to use
   [PyCharm](https://www.jetbrains.com/pycharm/) as your IDE refer to
   [using PyCharm IDE](https://cyberbotics.com/doc/guide/using-your-ide#pycharm)
   provided by Webots

You will probably also need a backend library to implement the neural networks,
such as [PyTorch](https://pytorch.org/) or
[TensorFlow](https://www.tensorflow.org/). Deepbots interfaces with RL agents
using the gym logic, so it can work with any backend library you choose
to implement the agent with and any agent that already works with gym, such
as [stable-baselines3](https://github.com/DLR-RM/stable-baselines3) 
implementations.

### Install deepbots

Deepbots can be installed through the package installer
[pip](https://pip.pypa.io/en/stable/) running the following command:

`pip install deepbots`

If you encounter [this](https://github.com/aidudezzz/deepbots/issues/143) 
issue please use `pip install setuptools==65.5.0` before installing deepbots.

## Official resources

- On
  [the deepbots-tutorials repository](https://github.com/aidudezzz/deepbots-tutorials)
  you can find the official tutorials for deepbots
- On [the deepworlds repository](https://github.com/aidudezzz/deepworlds) you
  can find examples of deepbots being used. <br>Feel free to contribute your
  own!

## Citation

Conference paper (AIAI2020):
https://link.springer.com/chapter/10.1007/978-3-030-49186-4_6

```bibtex
@InProceedings{10.1007/978-3-030-49186-4_6,
    author="Kirtas, M.
    and Tsampazis, K.
    and Passalis, N.
    and Tefas, A.",
    title="Deepbots: A Webots-Based Deep Reinforcement Learning Framework for Robotics",
    booktitle="Artificial Intelligence Applications and Innovations",
    year="2020",
    publisher="Springer International Publishing",
    address="Cham",
    pages="64--75",
    isbn="978-3-030-49186-4"
}

```

### Acknowledgments

This project has received funding from the European Union's Horizon 2020
research and innovation programme under grant agreement No 871449 (OpenDR).
This publication reflects the authors’ views only. The European Commission is
not responsible for any use that may be made of the information it contains.

## Contributors ✨

Thanks goes to these wonderful people
([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="http://eakirtas.webpages.auth.gr/"><img src="https://avatars.githubusercontent.com/u/10010230?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Manos Kirtas</b></sub></a><br /><a href="https://github.com/aidudezzz/deepbots/commits?author=ManosMagnus" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/tsampazk"><img src="https://avatars.githubusercontent.com/u/27914645?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Kostas Tsampazis</b></sub></a><br /><a href="https://github.com/aidudezzz/deepbots/commits?author=tsampazk" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/kelvin-yang-b7b508198/"><img src="https://avatars.githubusercontent.com/u/49781698?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jiun Kai Yang</b></sub></a><br /><a href="https://github.com/aidudezzz/deepbots/commits?author=KelvinYang0320" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/MentalGear"><img src="https://avatars.githubusercontent.com/u/2837147?v=4?s=100" width="100px;" alt=""/><br /><sub><b>MentalGear</b></sub></a><br /><a href="#ideas-MentalGear" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/DreamtaleCore"><img src="https://avatars.githubusercontent.com/u/12713528?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Dreamtale</b></sub></a><br /><a href="https://github.com/aidudezzz/deepbots/issues?q=author%3ADreamtaleCore" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://nickkok.github.io/my-website/"><img src="https://avatars.githubusercontent.com/u/8222731?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nikolaos Kokkinis-Ntrenis</b></sub></a><br /><a href="https://github.com/aidudezzz/deepbots/commits?author=NickKok" title="Code">💻</a> <a href="https://github.com/aidudezzz/deepbots/commits?author=NickKok" title="Documentation">📖</a> <a href="#ideas-NickKok" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the
[all-contributors](https://github.com/all-contributors/all-contributors)
specification. Contributions of any kind welcome!

<b> Special thanks to <a href='https://www.papanikolaouev.com/'>Papanikolaou Evangelia</a> </b> for designing project's logo! </b> 
