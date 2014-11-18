add_executable(monopoly main.cpp boardlocation.cpp game.cpp moneypool.cpp player.cpp success.cpp)

target_include_directories(monopoly PUBLIC ../include/game ../include/stats)