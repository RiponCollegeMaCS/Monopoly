add_executable(monopoly main.cpp game/boardlocation.cpp game/game.cpp game/moneypool.cpp game/player.cpp stats/success.cpp util/csv.cpp)

target_include_directories(monopoly PUBLIC ../include/game ../include/stats ../include/util)
