# SPDX-FileCopyrightText: 2026 Ingo Ruhnke <grumbel@gmail.com>
# SPDX-License-Identifier: GPL-3.0-or-later

cmake_minimum_required(VERSION 3.16)

# Source of truth: top-level VERSION (e.g. "0.4.0-dev"), or
# -DPROJECT_VERSION_FULL=... from packaging (Nix may append .<revCount>+g<rev>).
if(NOT DEFINED PROJECT_VERSION_FULL)
  file(STRINGS "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" PROJECT_VERSION_FULL LIMIT_COUNT 1)
endif()

# project() needs a numeric version; strip -dev / +git / similar suffixes.
string(REGEX MATCH "^[0-9]+(\\.[0-9]+)*" _project_version_cmake "${PROJECT_VERSION_FULL}")

project(qflashlight VERSION ${_project_version_cmake} LANGUAGES CXX)

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

target_compile_definitions(qflashlight PRIVATE
  QFLASHLIGHT_VERSION="${PROJECT_VERSION_FULL}"
)

target_include_directories(qflashlight PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)

include(GNUInstallDirs)

install(TARGETS qflashlight RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

install(FILES qflashlight.desktop
  DESTINATION ${CMAKE_INSTALL_DATADIR}/applications)

install(FILES data/qflashlight.svg
  DESTINATION ${CMAKE_INSTALL_DATADIR}/icons/hicolor/scalable/apps
  RENAME qflashlight.svg)
