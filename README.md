Fuse
==========

> Next generation face swapper and enhancer.

[![Build Status](https://img.shields.io/github/actions/workflow/status/fuse/fuse/ci.yml.svg?branch=master)](https://github.com/fuse/fuse/actions?query=workflow:ci)
![License](https://img.shields.io/badge/license-MIT-green)


Preview
-------

![Preview](https://raw.githubusercontent.com/fuse/fuse/master/.github/preview.png?sanitize=true)


Installation
------------

Be aware, the installation needs technical skills and is not for beginners. Please do not open platform and installation related issues on GitHub. We have a very helpful [Discord](https://join.fuse.io) community that will guide you to install Fuse.

Read the [installation](https://docs.fuse.io/installation) now.


Build for Linux
---------------

### Using GitHub Actions (Recommended)
1. Fork or push this repository to GitHub.
2. Go to the "Actions" tab.
3. Select the "Build Linux Executable" workflow.
4. Download the `fuse_linux_executable` artifact from the completed run.

### Using Google Colab (Easiest for Web Users)
If you don't use GitHub Actions or Docker, you can build on Google Colab:

1. Download the `build_on_colab.ipynb` file from this repository.
2. Go to [Google Colab](https://colab.research.google.com/).
3. Upload the notebook (File -> Upload notebook).
4. Run the cells in order. The last cell will download the `fuse_linux` executable to your computer.

### Using Docker
If you have Docker installed, you can build the Linux executable locally:

1. Build the image: `docker build -f Dockerfile.linux -t fuse-linux-builder .`
2. Create container: `docker create --name fuse_temp fuse-linux-builder`
3. Copy executable: `docker cp fuse_temp:/app/dist/fuse_linux ./fuse_linux`
4. Clean up: `docker rm fuse_temp`

Or simply run the provided script on Windows:
```cmd
build_linux_docker.bat
```


Usage
-----

Run the command:

```
python run.py [options]

options:
  -h, --help                                                                                       show this help message and exit
  -s SOURCE_PATH, --source SOURCE_PATH                                                             select a source image
  -t TARGET_PATH, --target TARGET_PATH                                                             select a target image or video
  -o OUTPUT_PATH, --output OUTPUT_PATH                                                             specify the output file or directory
  -v, --version                                                                                    show program's version number and exit

misc:
  --skip-download                                                                                  omit automate downloads and lookups
  --headless                                                                                       run the program in headless mode

execution:
  --execution-providers {cpu} [{cpu} ...]                                                          choose from the available execution providers (choices: cpu, ...)
  --execution-thread-count EXECUTION_THREAD_COUNT                                                  specify the number of execution threads
  --execution-queue-count EXECUTION_QUEUE_COUNT                                                    specify the number of execution queries
  --max-memory MAX_MEMORY                                                                          specify the maximum amount of ram to be used (in gb)

face recognition:
  --face-recognition {reference,many}                                                              specify the method for face recognition
  --face-analyser-direction {left-right,right-left,top-bottom,bottom-top,small-large,large-small}  specify the direction used for face analysis
  --face-analyser-age {child,teen,adult,senior}                                                    specify the age used for face analysis
  --face-analyser-gender {male,female}                                                             specify the gender used for face analysis
  --reference-face-position REFERENCE_FACE_POSITION                                                specify the position of the reference face
  --reference-face-distance REFERENCE_FACE_DISTANCE                                                specify the distance between the reference face and the target face
  --reference-frame-number REFERENCE_FRAME_NUMBER                                                  specify the number of the reference frame

frame extraction:
  --trim-frame-start TRIM_FRAME_START                                                              specify the start frame for extraction
  --trim-frame-end TRIM_FRAME_END                                                                  specify the end frame for extraction
  --temp-frame-format {jpg,png}                                                                    specify the image format used for frame extraction
  --temp-frame-quality [0-100]                                                                     specify the image quality used for frame extraction
  --keep-temp                                                                                      retain temporary frames after processing

output creation:
  --output-image-quality [0-100]                                                                   specify the quality used for the output image
  --output-video-encoder {libx264,libx265,libvpx-vp9,h264_nvenc,hevc_nvenc}                        specify the encoder used for the output video
  --output-video-quality [0-100]                                                                   specify the quality used for the output video
  --keep-fps                                                                                       preserve the frames per second (fps) of the target
  --skip-audio                                                                                     omit audio from the target

frame processors:
  --frame-processors FRAME_PROCESSORS [FRAME_PROCESSORS ...]                                       choose from the available frame processors (choices: face_enhancer, face_swapper, frame_enhancer, ...)
  --face-enhancer-model {codeformer,gfpgan_1.2,gfpgan_1.3,gfpgan_1.4,gpen_bfr_512}                 choose from the mode for the frame processor
  --face-enhancer-blend [0-100]                                                                    specify the blend factor for the frame processor
  --face-swapper-model {inswapper_128,inswapper_128_fp16}                                          choose from the mode for the frame processor
  --frame-enhancer-model {realesrgan_x2plus,realesrgan_x4plus,realesrnet_x4plus}                   choose from the mode for the frame processor
  --frame-enhancer-blend [0-100]                                                                   specify the blend factor for the frame processor

uis:
  --ui-layouts UI_LAYOUTS [UI_LAYOUTS ...]                                                         choose from the available ui layouts (choices: benchmark, webcam, default, ...)
```


Disclaimer
----------

We acknowledge the unethical potential of Fuse and are resolutely dedicated to establishing safeguards against such misuse. This program has been engineered to abstain from processing inappropriate content such as nudity, graphic content and sensitive material.

It is important to note that we maintain a strong stance against any type of pornographic nature and do not collaborate with any websites promoting the unauthorized use of our software.

Users who seek to engage in such activities will face consequences, including being banned from our community. We reserve the right to report developers on GitHub who distribute unlocked forks of our software at any time.


Documentation
-------------

Read the [documentation](https://docs.fuse.io) for a deep dive.
