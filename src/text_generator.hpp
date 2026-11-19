// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#ifndef QFLASHLIGHT_TEXT_GENERATOR_HPP
#define QFLASHLIGHT_TEXT_GENERATOR_HPP

#include <QObject>
#include <QString>
#include <QTimer>
#include <QProcess>
#include <functional>
#include <optional>

class TextGenerator : public QObject
{
  Q_OBJECT

public:
  TextGenerator(const QString& command,
                std::optional<double> intervalSec,
                std::function<void(const QString&)> callback,
                QObject* parent = nullptr);

  void start();
  void stop();

private slots:
  void runOnce();

private:
  QString m_command;
  std::optional<double> m_intervalSec;
  std::function<void(const QString&)> m_callback;
  QTimer m_timer;
  QProcess m_process;
};

#endif
