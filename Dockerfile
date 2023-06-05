FROM --platform=linux/amd64 ubuntu:rolling

RUN apt-get update && apt-get install -y python3.11 curl unzip openjdk-11-jdk expect libxdamage1/lunar pulseaudio libxcursor-dev/lunar libxcursor1:amd64 qemu-system-x86 libvirt-daemon-system libvirt-clients bridge-utils

RUN curl https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -o cmd-tools

RUN unzip cmd-tools -d /setUp; rm cmd-tools; mv /setUp/cmdline-tools /setUp/sdk

RUN mkdir /setUp/sdk/tools

COPY ./moveFiles.sh /

RUN chmod 755 /moveFiles.sh; bash -c "source moveFiles.sh; tools_sorting"

RUN curl https://dl.google.com/android/repository/platform-tools_r34.0.1-linux.zip -o platform-tools

RUN unzip platform-tools -d /setUp/sdk

ENV JAVA_HOME=/lib/jvm/java-11-openjdk-amd64

ENV ANDROID_HOME=/setUp/sdk
ENV ANDROID_SDK=/setUp/sdk
ENV ANDROID_SDK_ROOT=/setUp/sdk
ENV SDK_ROOT=/setUp/sdk

ENV PATH=$PATH:$ANDROID_HOME:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$JAVA_HOME

COPY ./src /project

COPY ./emulators /project/emulators

COPY ./acceptLicenses.sh /

ENV ANDROID_AVD_HOME=/project/emulators

ENV PATH=$PATH:$ANDROID_AVD_HOME

RUN chmod 755 acceptLicenses.sh

RUN ./acceptLicenses.sh "sdkmanager --sdk_root=/setUp/sdk/cmdline-tools/latest emulator"

RUN ./acceptLicenses.sh "sdkmanager --sdk_root=/setUp/sdk/cmdline-tools/latest system-images;android-33;google_apis;x86_64"

RUN ./acceptLicenses.sh "sdkmanager --sdk_root=/setUp/sdk/cmdline-tools/latest platforms;android-33"

RUN bash -c "source moveFiles.sh; sdk_sorting"

ENV PATH=$PATH:$ANDROID_SDK/emulator

WORKDIR /project


