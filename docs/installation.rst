Installation
============

.. _Prerequisites:

Prerequisites
-------------

#. `Install Webots <https://cyberbotics.com/doc/guide/installing-webots>`_

   * `Windows <https://cyberbotics.com/doc/guide/installation-procedure#installation-on-windows>`_
   * `Linux <https://cyberbotics.com/doc/guide/installation-procedure#installation-on-linux>`_
   * `macOS <https://cyberbotics.com/doc/guide/installation-procedure#installation-on-macos>`_

#. `Install Python version 3.X <https://www.python.org/downloads>`_ (please refer to
   `Using Python <https://cyberbotics.com/doc/guide/using-python#introduction>`_
   to select the proper Python version for your system)
#. Refer to the `Using Python <https://cyberbotics.com/doc/guide/using-python>`_
   guide provided by Webots
#. Webots provides a basic code editor, but if you want to use
   `PyCharm <https://www.jetbrains.com/pycharm>`_ as your IDE refer to
   `using PyCharm IDE <https://cyberbotics.com/doc/guide/using-your-ide#pycharm>`_
   provided by Webots

You will probably also need a backend library to implement the neural networks,
such as `PyTorch <https://pytorch.org>`_ or
`TensorFlow <https://www.tensorflow.org>`_. Deepbots interfaces with RL agents
using the gym logic, so it can work with any backend library you choose
to implement the agent with and any agent that already works with gym, such
as `stable-baselines3 <https://github.com/DLR-RM/stable-baselines3>`_
implementations.

Install deepbots
----------------

Deepbots can be installed through the package installer
`pip <https://pip.pypa.io/en/stable>`_ running the following command:

.. code-block:: bash

   pip install deepbots

If you encounter `this <https://github.com/aidudezzz/deepbots/issues/143>`_
issue please use :code:`pip install setuptools==65.5.0` before installing deepbots.

.. role:: bash(code)
   :language: bash