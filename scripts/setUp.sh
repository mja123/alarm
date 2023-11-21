#!/bin/zsh

function getTools() {
  curl https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -o cmd-tools
  curl https://dl.google.com/android/repository/platform-tools_r34.0.1-linux.zip -o platform-tools
  unzip cmd-tools -d ~/setUp
  unzip platform-tools -d ~/setUp
  rm cmd-tools
  rm platform-tools
}

function setEnvs() {
  chmod 755 /moveFiles.sh
  bash -c "source moveFiles.sh; tools_sorting"
  export ANDROID_HOME=~/setUp/sdk
  export ANDROID_SDK=~/setUp/sdk
  export ANDROID_SDK_ROOT=~/setUp/sdk
  export SDK_ROOT=~/setUp/sdk
  export PATH=$PATH:$ANDROID_HOME:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$JAVA_HOME
}

function installAndroidTools() {
  chmod 755 acceptLicenses.sh
  ./acceptLicenses.sh "sdkmanager --sdk_root=~/setUp/sdk/cmdline-tools/latest build-tools;33.0.2"
  ./acceptLicenses.sh "sdkmanager --sdk_root=~/setUp/sdk/cmdline-tools/latest system-images;android-33;google_apis;arm64-v8a"
  ./acceptLicenses.sh "sdkmanager --sdk_root=~/setUp/sdk/cmdline-tools/latest platforms;android-33"
  export PATH=$PATH:$ANDROID_SDK/emulator
}

getTools
setEnvs
installAndroidTools