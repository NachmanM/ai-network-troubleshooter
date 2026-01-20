FROM prom/snmp-generator:v0.30.1

# Install make and git (needed to fetch MIBs)
RUN apt-get update && apt-get install -y git make curl

# Create the MIB directory
WORKDIR /opt

# Clone the LibreNMS MIBs repository
# This is the "Central Repo" strategy. It contains MIBs for almost every vendor.
RUN git clone https://github.com/librenms/librenms-mibs.git mibs

# Tell the generator to look in this new folder for MIBs
# We append the new path to the MIBDIRS environment variable
ENV MIBDIRS /opt/mibs:/root/.snmp/mibs:/usr/share/snmp/mibs

# Copy your local generator config into the image
COPY generator.yml /opt/generator.yml

# We override the entrypoint to perform substitution BEFORE generating.
# It reads generator.yml.tmpl, fills in the secrets, saves it as generator.yml, 
# and THEN runs the standard generate command.
ENTRYPOINT ["/bin/bash", "-c", "envsubst < /opt/generator.yml.tmpl > /opt/generator.yml && generator generate --output-path=/output/snmp.yml"]
