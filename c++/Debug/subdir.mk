################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CPP_SRCS += \
../boardlocation.cpp \
../game.cpp \
../main.cpp \
../player.cpp \
../success.cpp 

OBJS += \
./boardlocation.o \
./game.o \
./main.o \
./player.o \
./success.o 

CPP_DEPS += \
./boardlocation.d \
./game.d \
./main.d \
./player.d \
./success.d 


# Each subdirectory must supply rules for building sources it contributes
%.o: ../%.cpp
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -O3 -g3 -Wall -c -fmessage-length=0 -std=c++11 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$(@:%.o=%.d)" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


