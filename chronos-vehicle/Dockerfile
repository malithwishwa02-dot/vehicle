FROM kasmweb/chrome:1.14.0
USER root

# [LAYER 1] SYSTEM HARDENING & TIME TOOLS
# - iptables: For TTL Spoofing (Windows Camouflage)
# - haveged: For Entropy (Crypto-Uniqueness)
# - libfaketime: For Temporal Manipulation
RUN apt-get update && apt-get install -y \
    iptables iproute2 haveged sudo \
    python3 python3-pip python3-dev git make gcc openssl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# [LAYER 2] COMPILE TIME MACHINE
WORKDIR /tmp
RUN git clone https://github.com/wolfcw/libfaketime.git && \
    cd libfaketime/src && make install && rm -rf /tmp/libfaketime

# [LAYER 3] PYTHON CONTROLLER ENV
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app ./app

# [LAYER 4] PERMISSIONS & CONFIG
# Create the time control pipe and grant Kasm user access
RUN mkdir -p /app/time_control && \
    chown -R 1000:1000 /app && \
    chmod 777 /app/time_control

# [LAYER 5] KERNEL INJECTION
# Preload the time library into the global environment
ENV LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1
ENV FAKETIME_FOLLOW_FILE=/app/time_control/chronos_clock
ENV FAKETIME_DONT_FAKE_MONOTONIC=1

# [LAYER 5.5] CHRONOS ADMINS
ENV CHRONOS_TOKEN=""

# [LAYER 6] BOOTLOADER
COPY entrypoint.sh /dockerstartup/custom_startup.sh
RUN chmod +x /dockerstartup/custom_startup.sh

USER 1000
ENTRYPOINT ["/dockerstartup/custom_startup.sh"]
