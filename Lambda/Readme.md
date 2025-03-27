# Lambda Functions Readme

There are 2 versions of the fake data script in this folder. One for running the function in Lambda and one for testing the function in linux command line environment. If running in the command line environment be sure to run the:
    - 'test_environment_setup.sh' script

This will configure the environment properly and install all the necessary packages for running file in Linux.

If running the file in Lambda go to the Layers folder and be sure to attach the faker_layer.zip file to your lambda function. For further detail see the readme in the Layers folder.