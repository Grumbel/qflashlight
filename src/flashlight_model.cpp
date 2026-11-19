// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#include "flashlight_model.hpp"

#include <QColor>
#include <Qt>

FlashlightModel::FlashlightModel(QObject* parent)
  : QObject(parent)
  , m_bg(Qt::black)
  , m_fg(Qt::white)
{
}

void FlashlightModel::setBackgroundColor(const QColor& c)
{
  if (m_bg != c) {
    m_bg = c;
    emit changed();
  }
}

void FlashlightModel::setForegroundColor(const QColor& c)
{
  if (m_fg != c) {
    m_fg = c;
    emit changed();
  }
}

void FlashlightModel::setFont(const QFont& f)
{
  m_font = f;
  emit changed();
}

void FlashlightModel::setText(const QString& t)
{
  if (m_text != t) {
    m_text = t;
    emit changed();
  }
}
