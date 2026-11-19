# SPDX-FileCopyrightText: 2026 Ingo Ruhnke <grumbel@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

cmake_minimum_required(VERSION 3.16)
project(qflashlight VERSION 0.3.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

add_executable(qflashlight
  src/main.cpp
  src/application.cpp
  src/application.hpp
  src/flashlight_model.cpp
  src/flashlight_model.hpp
  src/flashlight_widget.cpp
  src/flashlight_widget.hpp
  src/text_generator.cpp
  src/text_generator.hpp
)

target_link_libraries(qflashlight PRIVATE
  Qt6::Core
  Qt6::Gui
  Qt6::Widgets
)

target_include_directories(qflashlight PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

include(GNUInstallDirs)

install(TARGETS qflashlight RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

install(FILES qflashlight.desktop
  DESTINATION ${CMAKE_INSTALL_DATADIR}/applications)

install(FILES data/qflashlight.svg
  DESTINATION ${CMAKE_INSTALL_DATADIR}/icons/hicolor/scalable/apps
  RENAME qflashlight.svg)
