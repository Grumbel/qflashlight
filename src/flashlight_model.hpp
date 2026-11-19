// SPDX-FileCopyrightText: 2017-2026 Ingo Ruhnke <grumbel@gmail.com>
// SPDX-License-Identifier: GPL-3.0-or-later

#ifndef QFLASHLIGHT_FLASHLIGHT_MODEL_HPP
#define QFLASHLIGHT_FLASHLIGHT_MODEL_HPP

#include <QObject>
#include <QColor>
#include <QFont>
#include <QString>

class FlashlightModel : public QObject
{
  Q_OBJECT

public:
  explicit FlashlightModel(QObject* parent = nullptr);

  QColor backgroundColor() const { return m_bg; }
  QColor foregroundColor() const { return m_fg; }
  QFont font() const { return m_font; }
  QString text() const { return m_text; }

public slots:
  void setBackgroundColor(const QColor& c);
  void setForegroundColor(const QColor& c);
  void setFont(const QFont& f);
  void setText(const QString& t);

signals:
  void changed();

private:
  QColor m_bg;
  QColor m_fg;
  QFont m_font;
  QString m_text;
};

#endif
