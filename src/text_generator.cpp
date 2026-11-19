// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#include "text_generator.hpp"

#include <QProcess>

TextGenerator::TextGenerator(const QString& command,
                             std::optional<double> intervalSec,
                             std::function<void(const QString&)> callback,
                             QObject* parent)
  : QObject(parent)
  , m_command(command)
  , m_intervalSec(intervalSec)
  , m_callback(std::move(callback))
{
  connect(&m_timer, &QTimer::timeout, this, &TextGenerator::runOnce);
}

void TextGenerator::start()
{
  runOnce();
  if (m_intervalSec.has_value()) {
    m_timer.start(static_cast<int>(*m_intervalSec * 1000.0));
  }
}

void TextGenerator::stop()
{
  m_timer.stop();
}

void TextGenerator::runOnce()
{
  // Match Python subprocess.getoutput: shell, capture stdout+stderr
  QProcess proc;
  proc.start("sh", {"-c", m_command});
  proc.waitForFinished(-1);
  const QString out = QString::fromLocal8Bit(proc.readAllStandardOutput()
                                             + proc.readAllStandardError());
  if (m_callback) {
    m_callback(out);
  }
}
