# Base image is arm32v7 Alpine Linux on Docker Hub
FROM armhf/alpine

# Install tools needed to download and build the CHIP_IO library from source.
RUN apk update && apk add bison \
						  flex \
						  g++ \
						  gcc \
						  git \
						  make \
						  
		# Download python and tools for installing libraries
						  python-dev \
						  py-setuptools \
						  py-pip \

	# Some libraries for python are required, install them					  
	&&	pip install Flask requests \

		# Download source code for device tree compiler needed for CHIP_IO
	&&	git clone https://github.com/NextThingCo/dtc.git \
		
		# Build and install the device tree compiler
	&&	cd dtc && make && make install PREFIX=/usr  \
		
		# Remove the device tree compiler source code now that we've built it
	&&	cd .. \
	&&  rm dtc -rf \

		# Download the latest CHIP_IO source code
	&& git clone https://github.com/xtacocorex/CHIP_IO.git \
		
		# Install the CHIP_IO library from the proper directory
	&&	cd CHIP_IO && python setup.py install \
		
		# Remove CHIP_IO source code directory after it has been installed
	&&	cd ../ && rm -rf CHIP_IO \
		
		# Remove build tools, which are no longer needed after installation
	&&	apk del bison \
				flex \
				g++ \
				gcc \
				git \
				make 
				#py-setuptools \
				#py-pip

# Set and create a working directory called app
WORKDIR /app

RUN export SERVER="192.168.0.114"

# Copy the contents of the current directory into the working directory
ADD . /app				

CMD ["python", "rocket-buttons.py"]
