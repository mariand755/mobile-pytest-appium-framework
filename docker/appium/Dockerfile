FROM node:20-bullseye-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

# System dependencies (ARM adb comes from here)
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    android-sdk-platform-tools \
    curl \
    unzip \
    bash \
  && rm -rf /var/lib/apt/lists/*

# Use Debian SDK root so Appium can find adb
ENV ANDROID_SDK_ROOT=/usr/lib/android-sdk
ENV ANDROID_HOME=/usr/lib/android-sdk
ENV PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

# sdkmanager needs a writable HOME
ENV HOME=/tmp
RUN mkdir -p /tmp/.android && touch /tmp/.android/repositories.cfg

# Download Android command-line tools into the SAME SDK root
RUN mkdir -p $ANDROID_SDK_ROOT/cmdline-tools \
 && curl -sSL https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -o /tmp/cmdline-tools.zip \
 && unzip -q /tmp/cmdline-tools.zip -d $ANDROID_SDK_ROOT/cmdline-tools \
 && mv $ANDROID_SDK_ROOT/cmdline-tools/cmdline-tools $ANDROID_SDK_ROOT/cmdline-tools/latest \
 && rm /tmp/cmdline-tools.zip

# Accept licenses + install build-tools/platforms (into /usr/lib/android-sdk)
RUN yes | sdkmanager --sdk_root=${ANDROID_SDK_ROOT} --licenses

RUN sdkmanager --sdk_root=${ANDROID_SDK_ROOT} \
      "build-tools;34.0.0" \
      "platforms;android-34" \
   || true

# Verify apksigner exists
RUN ${ANDROID_SDK_ROOT}/build-tools/34.0.0/apksigner version

# Appium + UiAutomator2
RUN npm install -g appium@2.19.0 \
 && appium driver install uiautomator2@2.40.2

EXPOSE 4723
COPY docker/appium/start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]
