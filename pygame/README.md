# Space Invaders #

Command to generate the executable file on OSX

```shell
python3 setup.py bdist_mac

codesign --remove-signature build/space_invaders.app/Contents/MacOS/lib/Python

cp -r build/space_invaders.app ~/Desktop
```