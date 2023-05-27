FROM --platform=linux/amd64 ubuntu:rolling

RUN apt-get update && apt-get install -y python3.11 curl unzip openjdk-11-jdk expect

RUN curl https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -o cmd-tools

RUN unzip cmd-tools -d /setUp; rm cmd-tools; mv /setUp/cmdline-tools /setUp/sdk

RUN mkdir /setUp/sdk/tools

COPY ./moveFiles.sh /

RUN chmod 755 /moveFiles.sh; ./moveFiles.sh

RUN curl https://dl.google.com/android/repository/platform-tools_r34.0.1-linux.zip -o platform-tools

RUN unzip platform-tools -d /setUp/sdk

ENV JAVA_HOME="/lib/jvm/java-11-openjdk-amd64/"

ENV ANDROID_HOME="/setUp/sdk"

ENV SDK_ROOT=$ANDROID_HOME/cmdline-tools/latest

ENV PATH=$PATH:$ANDROID_HOME:$ANDROID_HOME/tools:$ANDROID_HOME/tools/bin:$ANDROID_HOME/platform-tools:$JAVA_HOME

COPY ./src /project

COPY ./acceptLicenses.sh /

RUN chmod 755 acceptLicenses.sh

RUN ./acceptLicenses.sh "sdkmanager --sdk_root=/setUp/sdk/cmdline-tools/latest emulator"

WORKDIR /project


